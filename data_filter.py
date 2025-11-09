import re
import unicodedata
import random
import os
from transformers import AutoTokenizer

INPUT_FILE = "data.txt" 
OUTPUT_DIR = "."        
MODEL_NAME = "ytu-ce-cosmos/turkish-gpt2-medium"  
MIN_TOKENS_FOR_TRAIN = 4
SEED = 42


TRAIN_RATIO = 0.8
VAL_RATIO = 0.1
TEST_RATIO = 0.1

random.seed(SEED)


tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

def normalize_unicode(text: str) -> str:
    """Unicode normalize NFKC"""
    return unicodedata.normalize("NFKC", text)

def clean_math_expressions(text: str) -> str:
    """Basit LaTeX ve matematiksel sembol temizlemeleri."""
    
    text = re.sub(r'\\frac\{(.*?)\}\{(.*?)\}', r'(\1 / \2)', text)
    
    text = re.sub(r'\$(.*?)\$', r'\1', text)
    
    text = re.sub(r'\\\[(.*?)\\\]', r'\1', text, flags=re.S)
    
    text = re.sub(r'(\w)\^\{(\d+)\}', r'\1 ** \2', text)
    text = re.sub(r'(\w)\^(\d+)', r'\1 ** \2', text)
    
    text = re.sub(r'\\', ' ', text)
    
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def normalize_numbers(text: str) -> str:
    """
    Binlik ayraçları ve ondalık ayraçlarını normalize et.
    Örn: "1.000.000" -> "1000000", "1,23" -> "1.23"
    (Basit heuristik — çok özel durumlara göre genişletilebilir.)
    """
    text = re.sub(r'(?<=\d)\.(?=\d{3}\b)', '', text)
    text = re.sub(r'(?<=\d),(?=\d)', '.', text)
    return text

def remove_headers(text: str) -> str:
    """PDF başlıkları, sayfa numaraları, 'Chapter' gibi kısımları temizle (basit regex)."""
    text = re.sub(r'Page\s*\d+', '', text, flags=re.I)
    text = re.sub(r'Sayfa\s*\d+', '', text, flags=re.I)
    text = re.sub(r'Chapter\s*\d+', '', text, flags=re.I)
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.M) 
    return text

def is_too_short_for_train(text: str, min_tokens: int = MIN_TOKENS_FOR_TRAIN) -> bool:
    """Tokenizer'a göre token sayısı < min_tokens ise True döner."""
    toks = tokenizer.tokenize(text)
    return len(toks) < min_tokens

if not os.path.exists(INPUT_FILE):
    raise FileNotFoundError(f"{INPUT_FILE} bulunamadı. Önce web_scraping/pdf_reading çalıştır.")

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    raw_lines = [line.strip() for line in f if line.strip()]


seen = set()
lines = []
for ln in raw_lines:
    if ln in seen:
        continue
    seen.add(ln)
    lines.append(ln)

print(f"Toplam ham satır (dedup sonrası): {len(lines)}")

cleaned = []
short_lines = []  
for line in lines:
    s = normalize_unicode(line)
    s = remove_headers(s)
    s = clean_math_expressions(s)
    s = normalize_numbers(s)
    s = s.strip()
    if not s:
        continue
    
    if is_too_short_for_train(s):
        short_lines.append(s)
    else:
        cleaned.append(s)

print(f"Cleaned (train'e uygun) satır sayısı: {len(cleaned)}")
print(f"Short lines (validation/test için saklandı): {len(short_lines)}")


n = len(cleaned)
n_train = int(TRAIN_RATIO * n)
n_val = int(VAL_RATIO * n)
train_data = cleaned[:n_train]
val_data = cleaned[n_train:n_train + n_val]
test_data = cleaned[n_train + n_val:]

if short_lines:
    random.shuffle(short_lines)
    half = len(short_lines) // 2
    val_data.extend(short_lines[:half])
    test_data.extend(short_lines[half:])

min_val_size = max(1, int(0.01 * len(cleaned)))  
if len(val_data) < min_val_size and len(train_data) > min_val_size:
    move = min_val_size - len(val_data)
    for _ in range(move):
        val_data.append(train_data.pop())

if len(test_data) < min_val_size and len(train_data) > min_val_size:
    move = min_val_size - len(test_data)
    for _ in range(move):
        test_data.append(train_data.pop())

print(f"Final split: Train={len(train_data)}, Val={len(val_data)}, Test={len(test_data)}")

os.makedirs(OUTPUT_DIR, exist_ok=True)

def write_list_to_file(lst, path):
    with open(path, "w", encoding="utf-8") as f:
        for line in lst:
            f.write(line.strip() + "\n\n")  

write_list_to_file(cleaned, os.path.join(OUTPUT_DIR, "cleaned_all.txt"))
write_list_to_file(train_data, os.path.join(OUTPUT_DIR, "train.txt"))
write_list_to_file(val_data, os.path.join(OUTPUT_DIR, "val.txt"))
write_list_to_file(test_data, os.path.join(OUTPUT_DIR, "test.txt"))

print("✅ Dosyalar oluşturuldu:")
print(" -", os.path.join(OUTPUT_DIR, "cleaned_all.txt"))
print(" -", os.path.join(OUTPUT_DIR, "train.txt"))
print(" -", os.path.join(OUTPUT_DIR, "val.txt"))
print(" -", os.path.join(OUTPUT_DIR, "test.txt"))
