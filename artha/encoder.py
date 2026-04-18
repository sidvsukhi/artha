import re

import tiktoken

TOKENIZER = tiktoken.get_encoding("cl100k_base")  # GPT-4 tokenizer

def token_count(text: str) -> int:
    return len(TOKENIZER.encode(text))

ACTIONS = {
    "summarize": "sum", "summarise": "sum",
    "generate": "gen", "write": "gen", "create": "gen", "draft": "gen",
    "fix": "fix", "debug": "fix", "correct": "fix", "repair": "fix",
    "explain": "xpl", "describe": "xpl", "what is": "xpl",
    "compare": "cmp", "contrast": "cmp", "diff": "cmp",
    "extract": "ext", "pull out": "ext", "find": "ext",
    "review": "rev", "critique": "rev", "evaluate": "rev",
    "format": "fmt", "structure": "fmt", "organise": "fmt",
    "rewrite": "ref", "rephrase": "ref", "reframe": "ref",
    "classify": "cls", "categorise": "cls", "categorize": "cls",
    "translate": "lang", "convert to": "lang",
    "rank": "rank", "order by": "rank", "sort by": "rank",
}

MODIFIERS = {
    "bullet points": "fmt:bullets", "bullets": "fmt:bullets",
    "numbered list": "fmt:list", "numbered steps": "fmt:steps",
    "table": "fmt:table", "json": "fmt:json", "markdown": "fmt:md",
    "formal": "tone:formal", "professional": "tone:professional",
    "casual": "tone:casual", "friendly": "tone:friendly",
    "simple": "lvl:simple", "technical": "lvl:technical",
    "python": "lang:py", "javascript": "lang:js",
    "typescript": "lang:ts", "rust": "lang:rs", "go": "lang:go",
}

FILLERS = [
    "please", "could you", "can you", "i want you to",
    "i would like you to", "i need you to", "make sure to",
    "ensure that", "you should", "try to", "attempt to",
    "the following", "as follows", "given the", "provided",
    "kindly", "i'd like", "would you", "help me",
]

CONSTRAINTS = {
    "focus on": "+", "emphasise": "+", "emphasize": "+",
    "prioritise": "+", "prioritize": "+", "especially": "+",
    "include": "+", "make sure to include": "+",
    "ignore": "-", "exclude": "-", "avoid": "-",
    "do not include": "-", "don't include": "-",
    "without": "-", "leave out": "-",
}

def encode(prompt: str) -> str:
    text = prompt.lower().strip()
    action = None
    modifiers = []
    constraints = []

    for filler in sorted(FILLERS, key=len, reverse=True):
        text = re.sub(rf'\b{re.escape(filler)}\b', '', text)

    for word, code in sorted(ACTIONS.items(), key=lambda x: len(x[0]), reverse=True):
        if word in text:
            action = code
            text = text.replace(word, '', 1).strip()
            break

    for word, code in sorted(MODIFIERS.items(), key=lambda x: len(x[0]), reverse=True):
        if word in text:
            modifiers.append(code)
            text = text.replace(word, '').strip()

    for word, symbol in sorted(CONSTRAINTS.items(), key=lambda x: len(x[0]), reverse=True):
        pattern = rf'{re.escape(word)}\s+([\w\s]+?)(?=[,.\n]|$)'
        matches = re.findall(pattern, text)
        for match in matches:
            topic = '_'.join(match.strip().split()[:2])
            constraints.append(f"{symbol}{topic}")
        text = re.sub(pattern, '', text).strip()

    text = re.sub(r'\b(\d+)\s*(bullet|point|item|word|sentence|line)s?', r'#\1', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = text.strip('.,; ')

    artha = action or 'gen'
    if text:
        artha += f'[{text}]'
    if modifiers:
        artha += f'({", ".join(modifiers)})'
    if constraints:
        artha += f' {" ".join(constraints)}'

    return artha

"""
def token_count(text: str) -> int:
    return len(text.strip().split())
"""

def compression_stats(original: str, compressed: str) -> dict:
    original_tokens = token_count(original)
    compressed_tokens = token_count(compressed)
    saved = original_tokens - compressed_tokens
    reduction = round((saved / original_tokens) * 100) if original_tokens > 0 else 0
    return {
        "original_tokens": original_tokens,
        "compressed_tokens": compressed_tokens,
        "saved": saved,
        "reduction_pct": reduction,
        "cost_saving_per_1M_calls": round((saved / 1000) * 0.01 * 1_000_000, 2)
    }
