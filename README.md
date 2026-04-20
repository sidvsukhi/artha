# ⟁ Artha
[![HuggingFace](https://img.shields.io/badge/🤗%20HuggingFace-siddsukh/artha--1.1b-yellow)](https://huggingface.co/siddsukh/artha-1.1b)
[![Demo](https://img.shields.io/badge/Live%20Demo-artha--demo-brightgreen)](https://huggingface.co/spaces/siddsukh/artha-demo)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/sidvsukhi/artha?style=social)](https://github.com/sidvsukhi/artha)

> Artha (Sanskrit: अर्थ) — meaning "essence", "purpose", "meaning"
> A token-efficient, math-based language for human-AI communication.

---

## The Idea

Why are we talking to AI in English?

There are 7,000 languages in the world. We picked English to talk 
to AI almost by accident — because that's what the training data 
was in. But what's truly universal across every language, every 
culture, every human mind?

**Mathematics and Logic.**

Artha is a compressed language built on mathematical notation where 
every token carries maximum meaning and nothing else survives.

---

## The Problem

Every token you send to an LLM costs money and time. But most 
prompts are full of waste:
"Please could you kindly summarise this article in bullet points"

Words like "please", "could you", "kindly" carry zero meaning 
for a machine. You're paying for every single one.

At scale:
1M API calls/day × 13 tokens avg = $4,745/month just on prompts
With Artha → $1,281/month
Saving     → $3,464/month ($41,568/year)

---

## How Artha Works
"Please summarise this article in 3 bullet points,
focus on key facts, ignore opinions"
→ sum[article](#3, fmt:bullets) +facts -opinions
"Fix the bug in this Python code and explain what was wrong"
→ fixcode → {diff+explain}
"Write a formal email to a client, under 150 words"
→ gen[eml](@client, tone:formal, ~150w)
"Compare React and Vue for a beginner, format as table"
→ cmp[React, Vue] → {table}

---

## Results

| Prompt Type | English Tokens | Artha Tokens | Saving |
|---|---|---|---|
| Summarisation | 12 | 3 | 75% |
| Code fix | 12 | 3 | 75% |
| Email generation | 14 | 3 | 79% |
| Comparison | 10 | 4 | 60% |
| Explanation | 11 | 3 | 73% |
| **Average** | **12** | **3** | **73%** |

---

## Key Insight

Compression only works when the model is **natively trained** 
on the language.
English tokenizer:  "fmt:bullets" = 4 tokens
Artha tokenizer:    "fmt:bullets" = 1 token

The model doesn't translate — it **thinks** natively in Artha.

---

## Quick Start

```bash
git clone https://github.com/sidvsukhi/artha.git
cd artha
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

Run the encoder:
```bash
python3 -c "
from artha.encoder import encode, compression_stats
prompt = 'Please summarise this in 3 bullet points, focus on facts'
compressed = encode(prompt)
stats = compression_stats(prompt, compressed)
print(f'Original : {prompt}')
print(f'Artha    : {compressed}')
print(f'Saving   : {stats[\"reduction_pct\"]}%')
"
```

Use the trained model:
```python
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch

base = AutoModelForCausalLM.from_pretrained(
    "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    torch_dtype=torch.bfloat16,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("siddsukh/artha-1.1b")
base.resize_token_embeddings(len(tokenizer), mean_resizing=False)
model = PeftModel.from_pretrained(base, "siddsukh/artha-1.1b")
model.eval()

def compress(prompt):
    input_text = f"<|artha|>\n{prompt}\n<|compress|>\n"
    inputs = tokenizer(input_text, return_tensors="pt").to(
        next(model.parameters()).device
    )
    with torch.no_grad():
        outputs = model.generate(
            **inputs, max_new_tokens=64,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=False)
    return decoded.split("<|compress|>")[-1].split("<|end|>")[0].strip()

print(compress("Please summarise this in 3 bullet points, focus on facts"))
# → sum[this](#3, fmt:bullets) +facts
```

---

## What We Built

### 1. Language Spec (`SPEC.md`)
The constitution of Artha. 60+ actions, modifiers, constraints, 
data types and control flow. Designed from first principles like 
a math notation system.

### 2. Corpus Generator (`artha/corpus.py`)
Generates English↔Artha training pairs at scale. 50,000 pairs 
across 13 action types.

### 3. Custom BPE Tokenizer (`artha/tokenizer.py`)
Trained from scratch on Artha corpus. Vocabulary: 1,124 tokens.
`fmt:bullets` = 1 token, not 4.

### 4. Fine-tuned Model (`artha/finetune.py`)
TinyLlama 1.1B fine-tuned on 50,000 Artha pairs using LoRA 
on TPU v5e. Available on HuggingFace.

### 5. Gateway (`artha/gateway.py`)
Drop-in middleware. Sits between your app and any LLM.
Compresses prompts automatically.

```python
from artha import Artha

artha = Artha(model="llama3.2:latest")
result = artha.chat("Please summarise this in 3 bullet points")
print(result["response"])
print(result["artha"]["stats"])
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
│   ├── tokenizer.py     ← custom BPE tokenizer
│   └── finetune.py      ← LoRA fine-tuning pipeline
├── examples/
│   ├── basic.py
│   ├── generate_corpus.py
│   ├── train_tokenizer.py
│   ├── finetune.py
│   ├── inference.py
│   └── artha_colab.ipynb  ← Google Colab notebook
└── data/                ← generated, not committed
├── corpus.jsonl
├── artha-tokenizer.json
└── artha-model/

---

## Roadmap

- [x] Language specification (v0.1.0)
- [x] Rule-based encoder
- [x] Corpus generator (50k pairs)
- [x] Custom BPE tokenizer
- [x] LoRA fine-tuning pipeline
- [x] Trained model on HuggingFace
- [x] 73% compression achieved
- [ ] arXiv paper
- [ ] pip package (`pip install artha`)
- [ ] OpenAI-compatible API gateway
- [ ] Browser extension
- [ ] Larger model (7B)
- [ ] 500k training pairs

---

## The Deeper Question

Is English actually the right substrate for human-AI communication?

We didn't choose it deliberately. We inherited it. Artha is an 
attempt to question that assumption — to ask what a language 
designed from scratch for AI communication would look like.

The answer, it turns out, looks a lot like mathematics.

---

## License

MIT — use it, build on it, make it better.

## Contributing

The language spec is the most important thing to get right.
Open an issue if you have ideas for improving the grammar.
This should be a community standard, not a personal project.

## Model

🤗 [siddsukh/artha-1.1b](https://huggingface.co/siddsukh/artha-1.1b)