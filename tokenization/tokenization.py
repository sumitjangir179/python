import tiktoken

tokenizer = tiktoken.encoding_for_model("gpt-4o")

text = "Hello, how are you?"

tokens = tokenizer.encode(text)

print(f"Tokenizer: {tokenizer}")
print(f"Tokens: {tokens}")
print(f"Token count: {len(tokens)}")