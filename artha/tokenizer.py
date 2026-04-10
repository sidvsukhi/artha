from tokenizers import Tokenizer, models, trainers, pre_tokenizers, decoders, processors
from tokenizers.normalizers import Lowercase
import json
import os

SPECIAL_TOKENS = [
    "[PAD]", "[UNK]", "[BOS]", "[EOS]", "[MASK]",
]

ARTHA_SYMBOLS = [
    "sum", "gen", "fix", "xpl", "cmp", "rev", "ext", "cls",
    "rank", "fmt", "ref", "opt", "exp", "cut", "mrg", "spl",
    "tns", "cnv", "fil", "tag", "anl", "inf", "val", "prd",
    "hyp", "dbg", "bch", "tst", "scr", "map", "qry", "agg",
    "srt", "idx", "jn", "trn", "nrm", "enc", "dec", "prs",
    "impl", "rfct", "doc", "test", "sec", "perf", "mig", "dep",
    "api", "eml", "msg", "rpt", "pch", "bio", "pst", "thr",
    "pln", "str", "brk", "est", "sim", "rsn", "arg", "cnt",
    "pro",
    "fmt:bullets", "fmt:list", "fmt:table", "fmt:json", "fmt:md",
    "fmt:html", "fmt:csv", "fmt:steps", "fmt:tldr", "fmt:qa",
    "fmt:dialog", "fmt:code", "fmt:diff", "fmt:outline",
    "tone:formal", "tone:casual", "tone:professional", "tone:friendly",
    "tone:assertive", "tone:empathetic", "tone:humorous", "tone:academic",
    "tone:persuasive", "tone:neutral",
    "lvl:eli5", "lvl:simple", "lvl:mid", "lvl:expert", "lvl:beginner",
    "lvl:advanced",
    "lang:en", "lang:fr", "lang:es", "lang:de", "lang:hi",
    "lang:zh", "lang:ar", "lang:pt", "lang:ja",
    "code:py", "code:js", "code:ts", "code:rs", "code:go",
    "code:java", "code:cpp", "code:sql", "code:sh",
    "@dev", "@mgr", "@client", "@student", "@exec", "@public", "@expert",
    "doc", "code", "data", "img", "url", "txt", "pdf",
    "csv", "json", "sql", "pr", "repo", "err", "log",
    "{text}", "{json}", "{table}", "{bullets}", "{steps}",
    "{diff}", "{summary}", "{report}", "{code}", "{outline}",
    "{rec}", "{score}", "{bool}", "{diff+explain}",
    ">>", "||", "→", "#each",
]

def build_tokenizer(vocab_size: int = 8000) -> Tokenizer:
    tokenizer = Tokenizer(models.BPE(unk_token="[UNK]"))
    tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)
    tokenizer.decoder = decoders.ByteLevel()
    return tokenizer

def train_tokenizer(
    corpus_path: str = "data/corpus.jsonl",
    output_path: str = "data/artha-tokenizer.json",
    vocab_size: int = 8000,
):
    print("Loading corpus...")
    corpus = []
    with open(corpus_path) as f:
        for line in f:
            item = json.loads(line)
            corpus.append(item["english"])
            corpus.append(item["artha"])

    print(f"Loaded {len(corpus)} texts ({len(corpus)//2} pairs)")

    tmp_path = "data/corpus_raw.txt"
    os.makedirs("data", exist_ok=True)
    with open(tmp_path, "w") as f:
        for text in corpus:
            f.write(text + "\n")

    print(f"Training BPE tokenizer (vocab_size={vocab_size})...")
    tokenizer = build_tokenizer(vocab_size)

    trainer = trainers.BpeTrainer(
        vocab_size=vocab_size,
        special_tokens=SPECIAL_TOKENS,
        initial_alphabet=pre_tokenizers.ByteLevel.alphabet(),
        show_progress=True,
    )

    tokenizer.train([tmp_path], trainer)

    print("Adding Artha special symbols to vocabulary...")
    tokenizer.add_tokens(ARTHA_SYMBOLS)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    tokenizer.save(output_path)
    print(f"Tokenizer saved to {output_path}")
    print(f"Final vocabulary size: {tokenizer.get_vocab_size()}")

    os.remove(tmp_path)
    return tokenizer


def load_tokenizer(path: str = "data/artha-tokenizer.json") -> Tokenizer:
    return Tokenizer.from_file(path)


def compare_tokenizers(text: str, artha_tokenizer: Tokenizer):
    import tiktoken
    en_tokenizer = tiktoken.get_encoding("cl100k_base")

    en_tokens = en_tokenizer.encode(text)
    ar_tokens = artha_tokenizer.encode(text).ids

    print(f"Text     : {text}")
    print(f"English  : {len(en_tokens)} tokens → {en_tokens[:10]}{'...' if len(en_tokens) > 10 else ''}")
    print(f"Artha    : {len(ar_tokens)} tokens → {ar_tokens[:10]}{'...' if len(ar_tokens) > 10 else ''}")
    saved = len(en_tokens) - len(ar_tokens)
    pct = round((saved / len(en_tokens)) * 100) if en_tokens else 0
    print(f"Saving   : {saved} tokens ({pct}%)")
    print()
