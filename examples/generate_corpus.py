import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from artha.corpus import generate_corpus, save_corpus, save_corpus_jsonl
import json

print("Generating Artha corpus...")
print()

# Preview 10 samples first
preview = generate_corpus(10)
print("SAMPLE PAIRS:")
print("=" * 60)
for i, pair in enumerate(preview, 1):
    print(f"{i}. EN: {pair['english']}")
    print(f"   AR: {pair['artha']}")
    print()

# Generate full corpus
print("=" * 60)
sizes = [1000, 5000, 10000, 50000]
size = int(sys.argv[1]) if len(sys.argv) > 1 else 10000

print(f"Generating {size} pairs...")
corpus = generate_corpus(size)

# Save in both formats
save_corpus(corpus, "data/corpus.json")
save_corpus_jsonl(corpus, "data/corpus.jsonl")

# Stats
print()
print("CORPUS STATS:")
print("=" * 60)
print(f"Total pairs     : {len(corpus)}")

avg_en = sum(len(p['english'].split()) for p in corpus) / len(corpus)
avg_ar = sum(len(p['artha'].split()) for p in corpus) / len(corpus)
reduction = round((1 - avg_ar/avg_en) * 100)

print(f"Avg English len : {avg_en:.1f} words")
print(f"Avg Artha len   : {avg_ar:.1f} words")
print(f"Avg compression : {reduction}%")
print()

# Show distribution
from collections import Counter
actions = Counter(p['artha'].split('[')[0] for p in corpus)
print("ACTION DISTRIBUTION:")
for action, count in actions.most_common():
    bar = "█" * (count // (size // 100))
    print(f"  {action:<8} {bar} {count}")
