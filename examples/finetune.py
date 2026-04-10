import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from artha.finetune import train

print("This will fine-tune Llama 3.2 1B on Artha corpus using LoRA.")
print("Expected time on Apple Silicon: ~30-60 minutes")
print("RAM required: ~8GB")
print()

model, tokenizer = train(
    corpus_path="data/corpus.jsonl",
    output_dir="data/artha-model",
    epochs=3,
    batch_size=2,
    lr=2e-4,
)

print()
print("Fine-tuning complete!")
print("Test it: python3 examples/inference.py")
