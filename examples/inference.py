import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

BASE_MODEL = "unsloth/Llama-3.2-1B"
ADAPTER_PATH = "data/artha-model"

print("Loading Artha model...")
tokenizer = AutoTokenizer.from_pretrained(ADAPTER_PATH)
base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    torch_dtype=torch.float32,
    device_map="auto",
)
model = PeftModel.from_pretrained(base_model, ADAPTER_PATH)
model.eval()
print("Model ready.")
print()

def compress(prompt: str) -> str:
    input_text = f"<|artha|>\n{prompt}\n<|compress|>\n"
    inputs = tokenizer(input_text, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=64,
            temperature=0.1,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=False)
    artha = decoded.split("<|compress|>")[-1].split("<|end|>")[0].strip()
    return artha


test_prompts = [
    "Please summarise this article in 3 bullet points, focus on key facts",
    "Fix the bug in this Python code and explain what was wrong",
    "Write a formal email to a client about the project delay, under 150 words",
    "Compare React and Vue for a beginner, format as table",
    "Explain machine learning to a 10 year old in simple language",
]

print("COMPRESSION TEST:")
print("=" * 60)
for prompt in test_prompts:
    compressed = compress(prompt)
    en_tokens = len(prompt.split())
    ar_tokens = len(compressed.split())
    saved = en_tokens - ar_tokens
    pct = round((saved / en_tokens) * 100)
    print(f"EN ({en_tokens:2d}t): {prompt}")
    print(f"AR ({ar_tokens:2d}t): {compressed}")
    print(f"Saved: {pct}%")
    print()
