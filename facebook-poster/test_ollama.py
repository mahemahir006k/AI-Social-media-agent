from caption_generator import call_ollama


prompt = """
Write a short professional Facebook caption
about recruitment trends.

Use a professional HR tone.

Keep it under 100 words.
"""


result = call_ollama(prompt)


print("\n==============================")
print("OLLAMA RESPONSE")
print("==============================\n")

print(result)