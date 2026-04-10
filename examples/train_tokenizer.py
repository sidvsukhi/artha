import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from artha.tokenizer import train_tokenizer, load_tokenizer, compare_tokenizers

print("=" * 60)
print("ARTHA TOKENIZER TRAINER")
print("=" * 60)
print()

tokenizer = train_tokenizer(
    corpus_path="data/corpus.jsonl",
    output_path="data/artha-tokenizer.json",
    vocab_size=8000,
)

print()
print("=" * 60)
print("TOKENIZER COMPARISON")
print("=" * 60)
print()

test_pairs = [
    ("sum[article](#3, fmt:bullets) +facts -opinions",
     "Please summarise this article in 3 bullet points, focus on key facts, ignore opinions"),
    ("fix[code](code:py) → {diff+explain}",
     "Fix the bug in this Python code and explain what was wrong"),
    ("gen[eml](@client, tone:formal, ~150w) +apologetic",
     "Write a formal email to a client, under 150 words, apologetic"),
    ("cmp[react, vue] → {table} +perf",
     "Compare React and Vue, format as table, focus on performance"),
    ("xpl[machine learning](lvl:beginner, fmt:bullets)",
     "Explain machine learning to a beginner using bullet points"),
]

print("ARTHA vs ENGLISH TOKEN COUNTS:")
print("-" * 60)

total_en = 0
total_ar = 0

for artha, english in test_pairs:
    en_tok = len(english.split())
    ar_tok = len(artha.split())
    total_en += en_tok
    total_ar += ar_tok
    saved = en_tok - ar_tok
    pct = round((saved / en_tok) * 100)
    print(f"EN ({en_tok:2d} tokens): {english[:60]}")
    print(f"AR ({ar_tok:2d} tokens): {artha}")
    print(f"Saving: {saved} tokens ({pct}%)")
    print()

print("-" * 60)
overall = round((1 - total_ar/total_en) * 100)
print(f"Overall compression: {overall}%")
print(f"Total EN tokens: {total_en}")
print(f"Total AR tokens: {total_ar}")
print(f"Total saved: {total_en - total_ar}")
print()
print("Tokenizer ready for model fine-tuning!")
print("Next step: python3 examples/finetune.py")
