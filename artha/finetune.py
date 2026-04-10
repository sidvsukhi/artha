import json
import os
import torch
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForSeq2Seq,
)
from peft import (
    LoraConfig,
    get_peft_model,
    TaskType,
    prepare_model_for_kbit_training,
)

MODEL_NAME = "unsloth/Llama-3.2-1B"
OUTPUT_DIR = "data/artha-model"

def load_corpus(path: str = "data/corpus.jsonl"):
    pairs = []
    with open(path) as f:
        for line in f:
            item = json.loads(line)
            pairs.append({
                "input": item["english"],
                "output": item["artha"],
            })
    print(f"Loaded {len(pairs)} training pairs")
    return pairs


def format_prompt(example):
    return {
        "text": f"<|artha|>\n{example['input']}\n<|compress|>\n{example['output']}<|end|>"
    }


def tokenize(example, tokenizer, max_length=128):
    result = tokenizer(
        example["text"],
        truncation=True,
        max_length=max_length,
        padding="max_length",
    )
    result["labels"] = result["input_ids"].copy()
    return result


def train(
    corpus_path: str = "data/corpus.jsonl",
    output_dir: str = OUTPUT_DIR,
    epochs: int = 3,
    batch_size: int = 4,
    lr: float = 2e-4,
):
    print("=" * 60)
    print("ARTHA MODEL FINE-TUNER")
    print("=" * 60)
    print()

    # ── Load corpus ───────────────────────────────────────────
    pairs = load_corpus(corpus_path)
    formatted = [format_prompt(p) for p in pairs]
    dataset = Dataset.from_list(formatted)
    split = dataset.train_test_split(test_size=0.05, seed=42)
    train_ds = split["train"]
    eval_ds = split["test"]
    print(f"Train: {len(train_ds)} | Eval: {len(eval_ds)}")
    print()

    # ── Load tokenizer ────────────────────────────────────────
    print(f"Loading tokenizer from {MODEL_NAME}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.add_special_tokens({
        "additional_special_tokens": ["<|artha|>", "<|compress|>", "<|end|>"]
    })
    print("Tokenizer loaded.")
    print()

    # ── Tokenize dataset ──────────────────────────────────────
    print("Tokenizing dataset...")
    train_ds = train_ds.map(
        lambda x: tokenize(x, tokenizer),
        batched=True,
        remove_columns=["text"]
    )
    eval_ds = eval_ds.map(
        lambda x: tokenize(x, tokenizer),
        batched=True,
        remove_columns=["text"]
    )
    print("Tokenization complete.")
    print()

    # ── Load model ────────────────────────────────────────────
    print(f"Loading base model {MODEL_NAME}...")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float32,
        device_map="auto",
    )
    model.resize_token_embeddings(len(tokenizer))
    print("Model loaded.")
    print()

    # ── Apply LoRA ────────────────────────────────────────────
    print("Applying LoRA adapters...")
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        target_modules=["q_proj", "v_proj"],
        bias="none",
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    print()

    # ── Training args ─────────────────────────────────────────
    args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        gradient_accumulation_steps=4,
        warmup_steps=50,
        learning_rate=lr,
        fp16=False,
        bf16=False,
        logging_steps=50,
        evaluation_strategy="steps",
        eval_steps=100,
        save_strategy="steps",
        save_steps=100,
        save_total_limit=2,
        load_best_model_at_end=True,
        report_to="none",
        optim="adamw_torch",
    )

    # ── Trainer ───────────────────────────────────────────────
    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=train_ds,
        eval_dataset=eval_ds,
        data_collator=DataCollatorForSeq2Seq(
            tokenizer,
            model=model,
            padding=True
        ),
    )

    # ── Train ─────────────────────────────────────────────────
    print("Starting training...")
    print()
    trainer.train()

    # ── Save ──────────────────────────────────────────────────
    os.makedirs(output_dir, exist_ok=True)
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    print()
    print(f"Model saved to {output_dir}")
    return model, tokenizer
