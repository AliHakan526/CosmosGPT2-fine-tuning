import matplotlib.pyplot as plt
import numpy as np


models = ['Base Model', 'Fine-tuned Model']
x = np.arange(len(models))


rouge_l = [0.04, 0.06]        
perplexity = [44.42, 20.20]   

width = 0.6

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

ax = axes[0]
bars = ax.bar(x, rouge_l, width)
ax.set_xticks(x)
ax.set_xticklabels(models)
ax.set_ylim(0, max(rouge_l) * 1.4)   
ax.set_ylabel('ROUGE-L')
ax.set_title('ROUGE-L Skorları')


for i, v in enumerate(rouge_l):
    ax.text(x[i], v + 0.002, f"{v:.2f}", ha='center', va='bottom', fontsize=10)

ax = axes[1]
bars = ax.bar(x, perplexity, width)
ax.set_xticks(x)
ax.set_xticklabels(models)
ax.set_ylim(0, max(perplexity) * 1.15)
ax.set_ylabel('Perplexity')
ax.set_title('Perplexity Değerleri')


for i, v in enumerate(perplexity):
    ax.text(x[i], v + max(perplexity)*0.02, f"{v:.2f}", ha='center', va='bottom', fontsize=10)

plt.suptitle('Model Karşılaştırması: Base vs Fine-tuned', fontsize=14)
plt.tight_layout(rect=[0, 0, 1, 0.95])


plt.show()

