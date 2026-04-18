import ollama
import os
import time
from artha.encoder import encode, compression_stats

DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:latest")

class Artha:
    def __init__(self, model: str = DEFAULT_MODEL, compress: bool = True):
        self.model = model
        self.compress = compress
        self._check_ollama()

    def _check_ollama(self):
        try:
            ollama.list()
        except Exception:
            raise RuntimeError("Ollama is not running. Start it with: ollama serve")

    def chat(self, prompt: str, stream: bool = False) -> dict:
        original = prompt
        compressed = encode(prompt) if self.compress else prompt
        stats = compression_stats(original, compressed) if self.compress else {}

        start = time.time()

        if stream:
            return self._stream(compressed, original, stats)

        response = ollama.chat(
            model=self.model,
            messages=[{"role": "user", "content": compressed}]
        )

        elapsed = round(time.time() - start, 2)
        content = response["message"]["content"]

        return {
            "response": content,
            "artha": {
                "original_prompt": original,
                "compressed_prompt": compressed,
                "stats": stats,
                "model": self.model,
                "elapsed_sec": elapsed
            }
        }

    def _stream(self, compressed: str, original: str, stats: dict):
        print(f"\n[Artha] Compressed: {compressed}")
        print(f"[Artha] Reduction: {stats.get('reduction_pct', 0)}%\n")
        for chunk in ollama.chat(
            model=self.model,
            messages=[{"role": "user", "content": compressed}],
            stream=True
        ):
            print(chunk["message"]["content"], end="", flush=True)
        print()
