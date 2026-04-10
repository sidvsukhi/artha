import random
import json
import os
from typing import List, Dict

# ── Vocabulary Banks ──────────────────────────────────────────

DOCUMENTS = ["doc", "article", "report", "essay", "paper", "text", "blog post", "readme"]
CODES = ["code", "function", "script", "class", "module", "snippet", "program"]
DATA = ["csv", "data", "dataset", "spreadsheet", "table", "json", "logs"]
EMAILS = ["email", "message", "reply", "response", "letter"]

TONES = [
    ("formal",       "tone:formal"),
    ("professional", "tone:professional"),
    ("casual",       "tone:casual"),
    ("friendly",     "tone:friendly"),
    ("assertive",    "tone:assertive"),
    ("empathetic",   "tone:empathetic"),
    ("academic",     "tone:academic"),
    ("persuasive",   "tone:persuasive"),
    ("neutral",      "tone:neutral"),
]

FORMATS = [
    ("bullet points",   "fmt:bullets"),
    ("numbered list",   "fmt:list"),
    ("a table",         "fmt:table"),
    ("JSON",            "fmt:json"),
    ("markdown",        "fmt:md"),
    ("numbered steps",  "fmt:steps"),
    ("a one liner",     "fmt:tldr"),
    ("Q&A format",      "fmt:qa"),
    ("an outline",      "fmt:outline"),
]

LEVELS = [
    ("a 5 year old",     "lvl:eli5"),
    ("a beginner",       "lvl:beginner"),
    ("a student",        "lvl:simple"),
    ("an intermediate",  "lvl:mid"),
    ("an expert",        "lvl:expert"),
]

LANGS = [
    ("French",     "lang:fr"),
    ("Spanish",    "lang:es"),
    ("German",     "lang:de"),
    ("Hindi",      "lang:hi"),
    ("Chinese",    "lang:zh"),
    ("Arabic",     "lang:ar"),
    ("Portuguese", "lang:pt"),
    ("Japanese",   "lang:ja"),
]

CODE_LANGS = [
    ("Python",     "code:py"),
    ("JavaScript", "code:js"),
    ("TypeScript", "code:ts"),
    ("Rust",       "code:rs"),
    ("Go",         "code:go"),
    ("Java",       "code:java"),
    ("SQL",        "code:sql"),
]

AUDIENCES = [
    ("developers",       "@dev"),
    ("managers",         "@mgr"),
    ("clients",          "@client"),
    ("students",         "@student"),
    ("executives",       "@exec"),
    ("the general public","@public"),
]

FILLERS = [
    "Please ", "Could you ", "Can you ", "I want you to ",
    "I need you to ", "Would you ", "Help me ", "Kindly ",
    "I'd like you to ", "I'd appreciate if you could ",
]

TOPICS = [
    "machine learning", "climate change", "quantum computing",
    "the French Revolution", "blockchain", "neural networks",
    "the stock market", "renewable energy", "cybersecurity",
    "product roadmap", "team performance", "sales data",
    "customer feedback", "project timeline", "API design",
]

CONSTRAINTS_POS = [
    ("focus on key facts",    "+facts"),
    ("focus on performance",  "+perf"),
    ("include examples",      "+examples"),
    ("include data points",   "+data"),
    ("emphasise security",    "+security"),
    ("prioritise clarity",    "+clarity"),
    ("focus on actionability","+actionable"),
]

CONSTRAINTS_NEG = [
    ("ignore opinions",       "-opinions"),
    ("avoid jargon",          "-jargon"),
    ("exclude formatting",    "-formatting"),
    ("no fluff",              "-fluff"),
    ("without passive voice", "-passive"),
    ("exclude style issues",  "-style"),
    ("no code comments",      "-comments"),
]

# ── Template Generators ───────────────────────────────────────

def r(lst): return random.choice(lst)
def maybe(lst, p=0.5): return r(lst) if random.random() < p else None
def filler(): return r(FILLERS) if random.random() < 0.7 else ""

def pair(english: str, artha: str) -> Dict:
    return {"english": english.strip(), "artha": artha.strip()}

# ── 1. Summarisation ──────────────────────────────────────────

def gen_summarise() -> Dict:
    doc = r(DOCUMENTS)
    n = r([2, 3, 4, 5])
    fmt_en, fmt_ar = r(FORMATS[:5])
    pos = maybe(CONSTRAINTS_POS)
    neg = maybe(CONSTRAINTS_NEG)

    english = f"{filler()}summarise this {doc} in {n} {fmt_en}"
    artha = f"sum[{doc}](#{n}, {fmt_ar})"

    constraints = []
    if pos: 
        english += f", {pos[0]}"
        constraints.append(pos[1])
    if neg:
        english += f", {neg[0]}"
        constraints.append(neg[1])
    if constraints:
        artha += f" {' '.join(constraints)}"

    return pair(english, artha)

# ── 2. Generation ─────────────────────────────────────────────

def gen_generate() -> Dict:
    topic = r(TOPICS)
    fmt_en, fmt_ar = r(FORMATS)
    tone_en, tone_ar = r(TONES)
    audience_en, audience_ar = r(AUDIENCES)
    words = r([100, 150, 200, 300, 500])

    english = f"{filler()}write a {tone_en} piece about {topic} for {audience_en}, format as {fmt_en}, under {words} words"
    artha = f"gen[{topic}]({tone_ar}, {fmt_ar}, {audience_ar}, ~{words}w)"

    return pair(english, artha)

# ── 3. Code Fix ───────────────────────────────────────────────

def gen_fix() -> Dict:
    lang_en, lang_ar = r(CODE_LANGS)
    explain = random.random() < 0.6

    english = f"{filler()}fix the bug in this {lang_en} code"
    artha = f"fix[code]({lang_ar})"

    if explain:
        english += " and explain what was wrong"
        artha += " → {diff+explain}"
    else:
        artha += " → {diff}"

    return pair(english, artha)

# ── 4. Explanation ────────────────────────────────────────────

def gen_explain() -> Dict:
    topic = r(TOPICS)
    level_en, level_ar = r(LEVELS)
    fmt_en, fmt_ar = r(FORMATS[:6])

    english = f"{filler()}explain {topic} to {level_en} using {fmt_en}"
    artha = f"xpl[{topic}]({level_ar}, {fmt_ar})"

    return pair(english, artha)

# ── 5. Comparison ─────────────────────────────────────────────

def gen_compare() -> Dict:
    items = random.sample(TOPICS, 2)
    fmt_en, fmt_ar = r(FORMATS[:5])
    pos = maybe(CONSTRAINTS_POS)

    english = f"{filler()}compare {items[0]} and {items[1]}, format as {fmt_en}"
    artha = f"cmp[{items[0]}, {items[1]}] → {{{fmt_ar.split(':')[1]}}}"

    if pos:
        english += f", {pos[0]}"
        artha += f" {pos[1]}"

    return pair(english, artha)

# ── 6. Translation ────────────────────────────────────────────

def gen_translate() -> Dict:
    lang_en, lang_ar = r(LANGS)
    tone_en, tone_ar = r(TONES)
    words = r([100, 150, 200])

    english = f"{filler()}translate this text to {lang_en}, keep it {tone_en}, under {words} words"
    artha = f"tns[txt](lang:{lang_ar.split(':')[1]}, {tone_ar}) <{words}w"

    return pair(english, artha)

# ── 7. Email Generation ───────────────────────────────────────

def gen_email() -> Dict:
    audience_en, audience_ar = r(AUDIENCES)
    tone_en, tone_ar = r(TONES)
    words = r([100, 150, 200])
    pos = maybe(CONSTRAINTS_POS)

    english = f"{filler()}write a {tone_en} email to {audience_en}, under {words} words"
    artha = f"gen[eml]({audience_ar}, {tone_ar}, ~{words}w)"

    if pos:
        english += f", {pos[0]}"
        artha += f" {pos[1]}"

    return pair(english, artha)

# ── 8. Code Review ────────────────────────────────────────────

def gen_review() -> Dict:
    lang_en, lang_ar = r(CODE_LANGS)
    pos = maybe(CONSTRAINTS_POS, 0.8)
    neg = maybe(CONSTRAINTS_NEG, 0.6)

    english = f"{filler()}review this {lang_en} code"
    artha = f"rev[code]({lang_ar})"

    constraints = []
    if pos:
        english += f", {pos[0]}"
        constraints.append(pos[1])
    if neg:
        english += f", {neg[0]}"
        constraints.append(neg[1])
    if constraints:
        artha += f" {' '.join(constraints)} → {{report}}"

    return pair(english, artha)

# ── 9. Data Analysis ──────────────────────────────────────────

def gen_analyse() -> Dict:
    data_type = r(["csv", "data", "dataset", "json", "logs"])
    fmt_en, fmt_ar = r(FORMATS[:4])
    pos = maybe(CONSTRAINTS_POS)

    english = f"{filler()}analyse this {data_type} and output as {fmt_en}"
    artha = f"anl[{data_type}]({fmt_ar}) → {{json+summary}}"

    if pos:
        english += f", {pos[0]}"
        artha += f" {pos[1]}"

    return pair(english, artha)

# ── 10. Planning ──────────────────────────────────────────────

def gen_plan() -> Dict:
    audience_en, audience_ar = r(AUDIENCES)
    months = r([1, 3, 6, 12])
    fmt_en, fmt_ar = r([
        ("outline", "fmt:outline"),
        ("bullet points", "fmt:bullets"),
        ("numbered steps", "fmt:steps"),
    ])

    english = f"{filler()}create a {months} month roadmap for {audience_en}, format as {fmt_en}"
    artha = f"pln[roadmap](#{months}m, {audience_ar}, {fmt_ar}) +milestones"

    return pair(english, artha)

# ── 11. Control Flow ──────────────────────────────────────────

def gen_sequence() -> Dict:
    lang_en, lang_ar = r(CODE_LANGS)
    english = f"{filler()}fix this {lang_en} code then document it"
    artha = f"fix[code]({lang_ar}) >> doc[code] → {{md}}"
    return pair(english, artha)

def gen_conditional() -> Dict:
    lang_en, lang_ar = r(CODE_LANGS)
    english = f"if this {lang_en} code has errors fix them, otherwise document it"
    artha = f"val[code]({lang_ar}) ? fix[code] : doc[code]"
    return pair(english, artha)

def gen_loop() -> Dict:
    doc = r(DOCUMENTS)
    n = r([2, 3, 4])
    english = f"{filler()}summarise each of these {doc}s in {n} bullet points"
    artha = f"sum[{doc}*] #each(#{n}, fmt:bullets)"
    return pair(english, artha)

# ── Main Generator ────────────────────────────────────────────

GENERATORS = [
    (gen_summarise,  0.15),
    (gen_generate,   0.12),
    (gen_fix,        0.12),
    (gen_explain,    0.12),
    (gen_compare,    0.10),
    (gen_translate,  0.08),
    (gen_email,      0.08),
    (gen_review,     0.08),
    (gen_analyse,    0.07),
    (gen_plan,       0.04),
    (gen_sequence,   0.02),
    (gen_conditional,0.01),
    (gen_loop,       0.01),
]

def generate_corpus(n: int = 10000) -> List[Dict]:
    corpus = []
    generators, weights = zip(*GENERATORS)

    for _ in range(n):
        gen_fn = random.choices(generators, weights=weights, k=1)[0]
        try:
            corpus.append(gen_fn())
        except Exception:
            pass

    return corpus


def save_corpus(corpus: List[Dict], path: str = "data/corpus.json"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(corpus, f, indent=2)
    print(f"Saved {len(corpus)} pairs to {path}")


def save_corpus_jsonl(corpus: List[Dict], path: str = "data/corpus.jsonl"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        for item in corpus:
            f.write(json.dumps(item) + "\n")
    print(f"Saved {len(corpus)} pairs to {path}")
