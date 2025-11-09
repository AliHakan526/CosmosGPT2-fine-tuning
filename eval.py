# eval.py
import torch
import math
from transformers import AutoTokenizer, AutoModelForCausalLM
from rouge_score import rouge_scorer
from peft import PeftModel

device = "cuda" if torch.cuda.is_available() else "cpu"


model_name = "ytu-ce-cosmos/turkish-gpt2-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name).to(device)

lora_path = "results_lora"
model = PeftModel.from_pretrained(model, lora_path)
model = model.merge_and_unload()

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
model.eval()


with open("test.txt", "r", encoding="utf-8") as f:
    test_lines = [l.strip() for l in f if l.strip()]


def split_prefix_completion(sentence, ratio=0.6):
    words = sentence.split()
    if len(words) < 4:
        return None
    cut = max(1, int(len(words) * ratio))
    prefix = " ".join(words[:cut])
    completion = " ".join(words[cut:])
    return prefix, completion

pairs = [split_prefix_completion(s) for s in test_lines]
pairs = [p for p in pairs if p is not None]


scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
results = []

for prefix, true_completion in pairs:
    print(prefix)
    # tokenize prefix
    inputs = tokenizer(prefix, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=50,
            do_sample=False,
            eos_token_id=tokenizer.eos_token_id
        )
    generated_ids = outputs[0][inputs["input_ids"].shape[-1]:] 
    pred = tokenizer.decode(generated_ids, skip_special_tokens=True).strip()

    results.append((prefix, true_completion, pred))


total_rouge = 0
for prefix, true_completion, pred in results:
    score = scorer.score(true_completion, pred)
    print("PREFIX:", prefix)
    print("REF:", true_completion)
    print("PRED:", pred)
    print("ROUGE-L:", score['rougeL'].fmeasure)
    total_rouge = total_rouge + score["rougeL"].fmeasure
    print("------")

total_rouge = total_rouge / len(results)


def total_ppl_of_texts(texts, batch_size=8):
    model.eval()
    total_loss = 0.0
    total_tokens = 0

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        enc = tokenizer(batch, return_tensors="pt", padding=True, truncation=True, max_length=128).to(device)


        enc = {k: v.to(device) for k, v in enc.items()} 

        with torch.no_grad():
            outputs = model(**enc, labels=enc["input_ids"])
            loss = outputs.loss  
            num_tokens = (enc["attention_mask"] == 1).sum().item()

            total_loss += loss.item() * num_tokens
            total_tokens += num_tokens

    avg_loss = total_loss / total_tokens
    total_ppl = math.exp(avg_loss)
    return total_ppl


ppl_value = total_ppl_of_texts(test_lines)
print("Model Perplexity:", ppl_value)

with open("trained_results","w",encoding="utf-8") as f:
    f.write(f"Average ROUGE-L: {total_rouge}\n")
    f.write(f"Average perplexity: {ppl_value}")

    