from transformers import AutoTokenizer

print("Downloading manga-ocr tokenizer...")
tokenizer = AutoTokenizer.from_pretrained("kha-white/manga-ocr-base", use_fast=False)
print("Done!")