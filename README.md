# ⟁ Artha
> A token-efficient communication protocol for human-AI interaction

**Artha** (Sanskrit: अर्थ) means *"essence", "purpose", "meaning"* — which is exactly what this language is. Strip everything down to pure meaning. Nothing else survives.

---

## The Problem

Every token you send to an LLM costs money and time. But most prompts are full of waste:
"Please could you kindly summarise this article in bullet points"

Words like "please", "could you", "kindly" carry **zero meaning** for a machine. They're human social conventions — and you're paying for every single one.

At scale this adds up fast:
1M API calls/day × 13 tokens avg = $4,745/month just on prompts

---

## The Solution

Artha is a compressed language where every token carries maximum meaning:
English: "Please summarise this article in 3 bullet points, focus on key facts, ignore opinions"
Artha:   "sum[article](#3, fmt:bullets) +facts -opinions"
Saving:  71% fewer tokens. Same output. Every single call.

---

## How It Works
┌─────────────────────────────────────┐
│  You write normal English           │
├─────────────────────────────────────┤
│  Artha encoder compresses it        │  ← rule-based + ML
├─────────────────────────────────────┤
│  Artha-native tokenizer             │  ← custom BPE trained on Artha
├─────────────────────────────────────┤
│  Artha-native LLM                   │  ← fine-tuned on Artha corpus
├─────────────────────────────────────┤
│  Response returned in English       │
└─────────────────────────────────────┘

The key insight: **compression only works when the tokenizer and model are trained on Artha natively.** A standard English tokenizer sees `fmt:bullets` as 4 tokens. An Artha tokenizer sees it as 1.

---

## Results

| Prompt Type | English Tokens | Artha Tokens | Saving |
|---|---|---|---|
| Summarisation | 18 | 4 | 71% |
| Code fix | 12 | 3 | 75% |
| Email generation | 11 | 4 | 64% |
| Comparison | 10 | 5 | 50% |
| Explanation | 9 | 3 | 67% |
| **Average** | **12.4** | **3.9** | **66%** |

*Measured across 10,000 generated pairs using word-level counting.
Real token savings with Artha-native model pending benchmark (in progress).*

---

## What We Built

### 1. Language Spec (`SPEC.md`)
The constitution of Artha. Defines 60+ actions, modifiers, constraints, data types, and control flow. Designed from first principles — every symbol earns its place.
sum[doc](#3, fmt:bullets) +facts -opinions
fixcode → {diff+explain}
gen[eml](@client, tone:formal, ~150w) +apologetic
cmp[react, vue] → {table} +perf
xplconcept → {simple}

### 2. Encoder (`artha/encoder.py`)
Compiles English prompts into Artha notation. Rule-based with pattern matching — the foundation for the ML encoder.

### 3. Gateway (`artha/gateway.py`)
Drop-in middleware layer. Sits between your app and any LLM. Compresses prompts automatically — zero changes to your code.

```python
from artha import Artha

artha = Artha(model="llama3.2:latest")
result = artha.chat("Please summarise this in 3 bullet points")

print(result["response"])
print(result["artha"]["stats"])
```

### 4. Corpus (`artha/corpus.py`)
Generates English ↔ Artha training pairs at scale. Currently 10,000 pairs across 13 action types with weighted distribution.

```json
{
  "english": "Please summarise this article in 3 bullets, focus on facts",
  "artha": "sum[article](#3, fmt:bullets) +facts"
}
```

### 5. Custom BPE Tokenizer (`artha/tokenizer.py`)
Trained from scratch on the Artha corpus. Vocabulary size: 1,121 tokens. Every Artha symbol (`fmt:bullets`, `tone:formal`, `code:py`) is a single token — not 4.

### 6. Fine-tuned LLM (`artha/finetune.py`)
TinyLlama 1.1B fine-tuned on 9,500 Artha pairs using LoRA. Trains in ~45 minutes on Apple Silicon. The model natively understands and generates Artha.

---

## Quick Start

```bash
# Clone
git clone https://github.com/yourusername/artha.git
cd artha

# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .

# Generate corpus
python3 examples/generate_corpus.py 10000

# Train tokenizer
python3 examples/train_tokenizer.py

# Fine-tune model (requires ~8GB RAM, 45 mins on Apple Silicon)
python3 examples/finetune.py

# Run inference
python3 examples/inference.py
```

---

## Project Structure
artha/
├── SPEC.md              ← language specification
├── artha/
│   ├── encoder.py       ← English → Artha compiler
│   ├── decoder.py       ← Artha → English
│   ├── gateway.py       ← drop-in LLM middleware
│   ├── corpus.py        ← training data generator
│   ├── tokenizer.py     ← custom BPE tokenizer trainer
│   └── finetune.py      ← LoRA fine-tuning pipeline
├── examples/
│   ├── basic.py         ← gateway demo
│   ├── generate_corpus.py
│   ├── train_tokenizer.py
│   ├── finetune.py
│   └── inference.py
└── data/                ← generated, not committed
├── corpus.jsonl
├── artha-tokenizer.json
└── artha-model/

---

## Roadmap

- [x] Language specification (v0.1.0)
- [x] Rule-based encoder
- [x] Ollama gateway
- [x] Corpus generator (10k pairs)
- [x] Custom BPE tokenizer
- [x] LoRA fine-tuning pipeline
- [ ] Artha-native model benchmark
- [ ] arXiv paper
- [ ] HuggingFace model release
- [ ] pip package (`pip install artha`)
- [ ] Browser extension
- [ ] OpenAI-compatible API gateway

---

## Origin

*First commit written at 35,000 feet on a flight to Dallas.*
*Because apparently that's when the best ideas happen.*

---

## License

MIT — use it, build on it, make it better.

---

## Contributing

The language spec is the most important thing to get right. If you have ideas for improving the grammar, open an issue. This should be a community standard, not a personal project.
