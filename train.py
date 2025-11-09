import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    EarlyStoppingCallback,
    TrainerCallback,
    DataCollatorForLanguageModeling
)
from datasets import load_dataset
from peft import LoraConfig, get_peft_model

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"✅ Eğitim cihazı: {device}")

dataset = load_dataset('text', data_files={'train': 'train.txt', 'validation': 'val.txt'})

model_name = "ytu-ce-cosmos/turkish-gpt2-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)


if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(model_name)
model.config.pad_token_id = tokenizer.pad_token_id

lora_config = LoraConfig(
    r=16,                      
    lora_alpha=32,             
    target_modules=["c_attn", "c_proj"], 
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)


model = get_peft_model(model, lora_config).to(device)
model.print_trainable_parameters() 

def tokenize_fn(batch):
    out = tokenizer(batch["text"], truncation=True, padding="max_length", max_length=256) # BURA
    out["labels"] = out["input_ids"].copy()
    return out

tokenized_ds = dataset.map(tokenize_fn, batched=True, remove_columns=["text"])
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

training_args = TrainingArguments(
    output_dir="./results_lora",
    eval_strategy="steps",
    eval_steps=500,       
    save_strategy="steps",
    save_steps=500,       
    save_total_limit=2,   
    learning_rate=2e-4,   
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=3, 
    weight_decay=0.01, 
    logging_dir='./logs_lora',
    logging_steps=100,
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
    greater_is_better=False,
    fp16=True if device == "cuda" else False,  
    seed=42
)

early_stopping = EarlyStoppingCallback(
    early_stopping_patience=2,
    early_stopping_threshold=0.0
)

class SaveLossesCallback(TrainerCallback):
    def __init__(self, log_file="loss_log.csv"):
        self.log_file = log_file
        with open(self.log_file, "w") as f:
            f.write("step,training_loss,validation_loss\n")

    def on_log(self, args, state, control, logs=None, **kwargs):
        if logs:
            step = state.global_step
            train_loss = logs.get("loss", "")
            val_loss = logs.get("eval_loss", "")
            with open(self.log_file, "a") as f:
                f.write(f"{step},{train_loss},{val_loss}\n")

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_ds["train"],
    eval_dataset=tokenized_ds["validation"],
    callbacks=[early_stopping,SaveLossesCallback()],
)

trainer.train()

model.save_pretrained(training_args.output_dir)   
tokenizer.save_pretrained(training_args.output_dir)

print("✅ LoRA fine-tuning tamamlandı. Model 'results_lora/' klasörüne kaydedildi.")
