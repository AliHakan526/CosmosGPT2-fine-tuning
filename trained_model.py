from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from peft import PeftModel
import torch

base_model = "ytu-ce-cosmos/turkish-gpt2-medium"
lora_path = "./results_lora/results_lora"


tokenizer = AutoTokenizer.from_pretrained(base_model)


model = AutoModelForCausalLM.from_pretrained(base_model, torch_dtype=torch.float16, device_map="auto")


model = PeftModel.from_pretrained(model, lora_path)



text_generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer
)


prompt = "integral"
result = text_generator(prompt, max_new_tokens=500, temperature=0.8, top_p=0.6)
print("input: ",prompt)
print("output: ",result[0]["generated_text"])