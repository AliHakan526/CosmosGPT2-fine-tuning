from transformers import AutoTokenizer, GPT2LMHeadModel
from transformers import pipeline

model = GPT2LMHeadModel.from_pretrained("ytu-ce-cosmos/turkish-gpt2-medium")
tokenizer = AutoTokenizer.from_pretrained("ytu-ce-cosmos/turkish-gpt2-medium")

text_generator = pipeline('text-generation', model=model, tokenizer=tokenizer)
input = "Bir fonksiyonun sürekli olması"
r = text_generator(input, max_length=100)
print("input: ",input)
print("output: ",r[0]["generated_text"])