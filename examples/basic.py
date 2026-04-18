from artha import Artha, encode, compression_stats

print("=" * 50)
print("ENCODER TEST")
print("=" * 50)

prompts = [
    "Please summarise this article in 3 bullet points, focus on key facts, ignore opinions",
    "Can you write a professional email to a client explaining the project delay, avoid jargon",
    "Fix the bug in this Python code and explain what was wrong",
    "Compare React and Vue, focus on performance, format as table",
]

for p in prompts:
    compressed = encode(p)
    stats = compression_stats(p, compressed)
    print(f"Original  : {p}")
    print(f"Artha     : {compressed}")
    print(f"Reduction : {stats['reduction_pct']}% ({stats['saved']} tokens saved)")
    print()

print("=" * 50)
print("GATEWAY TEST")
print("=" * 50)

artha = Artha(model="llama3.2:latest")

result = artha.chat(
    "Please summarise what machine learning is in 3 bullet points, simple language"
)

print(f"Original prompt  : {result['artha']['original_prompt']}")
print(f"Compressed prompt: {result['artha']['compressed_prompt']}")
print(f"Token reduction  : {result['artha']['stats']['reduction_pct']}%")
print(f"Response time    : {result['artha']['elapsed_sec']}s")
print(f"\nResponse:\n{result['response']}")
