import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("loss_log2.csv")


train_data = df.dropna(subset=["training_loss"])
val_data = df.dropna(subset=["validation_loss"])


plt.figure(figsize=(8,5))
plt.plot(train_data["step"], train_data["training_loss"], marker='o', linestyle='-', label="Training Loss")
plt.xlabel("Step")
plt.ylabel("Training Loss")
plt.title("Training Loss vs Step")
plt.grid(True)
plt.legend()
plt.show()


plt.figure(figsize=(8,5))
plt.plot(val_data["step"], val_data["validation_loss"], marker='o', linestyle='-', color='orange', label="Validation Loss")
plt.xlabel("Step")
plt.ylabel("Validation Loss")
plt.title("Validation Loss vs Step")
plt.grid(True)
plt.legend()
plt.show()

