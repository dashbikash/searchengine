import tiktoken
print(tiktoken.list_encoding_names())
enc=tiktoken.get_encoding("cl100k_base")

print([enc.decode_single_token_bytes(e).decode('utf-8') for e in enc.encode("welcome to my newworld")])