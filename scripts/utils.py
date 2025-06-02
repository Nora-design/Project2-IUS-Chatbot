from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

def count_tokens(text: str) -> int:
    return len(tokenizer.encode(text))