import matplotlib.pyplot as plt

PROBS = {
    "gene": {2: 0.01, 1: 0.03, 0: 0.96},
    "trait": {
        2: {True: 0.65, False: 0.35},
        1: {True: 0.56, False: 0.44},
        0: {True: 0.01, False: 0.99}
    },
    "mutation": 0.01
}

# Bar chart for gene probabilities
plt.figure(figsize=(10, 6))
plt.bar(PROBS["gene"].keys(), PROBS["gene"].values())
plt.xlabel('Number of Genes')
plt.ylabel('Probability')
plt.title('Unconditional Probabilities for Having Gene')
plt.show()

# Grouped bar chart for trait probabilities
labels = ['2 copies', '1 copy', 'No gene']
true_probs = [PROBS["trait"][2][True], PROBS["trait"][1][True], PROBS["trait"][0][True]]
false_probs = [PROBS["trait"][2][False], PROBS["trait"][1][False], PROBS["trait"][0][False]]

x = range(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, true_probs, width, label='Trait Present')
rects2 = ax.bar(x + width/2, false_probs, width, label='Trait Absent')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_xlabel('Gene Copies')
ax.set_ylabel('Probability')
ax.set_title('Probability of Trait Given Gene Copies')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

fig.tight_layout()


plt.savefig('visual.png')
plt.show()