import matplotlib.pyplot as plt
import pandas as pd
import ast

PATH = "C:/Users/simca/Google_Drive/WORK/Phd_project/Experimental/Fun-Landscapes/Library_Modelling/library_simulator/GA_output/"

SimpleParts_EntropyFitness_csv = "GA_SimpleParts_EntropyFitness_gens100_pop50.csv"
SimpleParts_NumFunsFitness_csv = "GA_SimpleParts_NumFunsFitness_gens100_pop50.csv"
SimpleParts_HybridFitness_csv = "GA_SimpleParts_HybridFitness_gens100_pop50.csv"
DoubleParts_HybridFitness_csv = "GA_DoubleParts_HybridFitness_gens100_pop50.csv"
TripleParts_HybridFitness_csv = "GA_TripleParts_HybridFitness_gens100_pop50.csv"

bar_name = "Final_Function_Distribution_Bars.png"

line_name = "Entropy_NumFuns_lines.png"

SimpleParts_EntropyFitness = pd.read_csv(PATH+SimpleParts_EntropyFitness_csv)
SimpleParts_NumFunsFitness = pd.read_csv(PATH+SimpleParts_NumFunsFitness_csv)
SimpleParts_HybridFitness = pd.read_csv(PATH+SimpleParts_HybridFitness_csv)
DoubleParts_HybridFitness = pd.read_csv(PATH+DoubleParts_HybridFitness_csv)
TripleParts_HybridFitness = pd.read_csv(PATH+TripleParts_HybridFitness_csv)



function_names = {
'FALSE': [[0], [0], [0], [0]],
'AND': [[0], [0], [0], [1]],
'A_ANDN_B': [[0], [0], [1], [0]],
'A': [[0], [0], [1], [1]],
'B_ANDN_A': [[0], [1], [0], [0]],
'B': [[0], [1], [0], [1]],
'XOR': [[0], [1], [1], [0]],
'OR': [[0], [1], [1], [1]],
'NOR': [[1], [0], [0], [0]],
'EQUALS': [[1], [0], [0], [1]],
'NOT_B': [[1], [0], [1], [0]],
'A_ORN_B': [[1], [0], [1], [1]],
'NOT_A': [[1], [1], [0], [0]],
'B_ORN_A': [[1], [1], [0], [1]],
'NAND': [[1], [1], [1], [0]],
'TRUE': [[1], [1], [1], [1]],
'CYCLIC': None
}


#### plotting ###

## plot 2 subplots, one for max shannon entropy v gens, one for max fun counts per gen
# Create subplots
plt.style.use('seaborn-colorblind')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

# shannon entropy plot on the left
ax1.plot(range(len(SimpleParts_EntropyFitness)), SimpleParts_EntropyFitness["entropy"])
ax1.plot(range(len(SimpleParts_NumFunsFitness)), SimpleParts_NumFunsFitness["entropy"])
ax1.plot(range(len(SimpleParts_HybridFitness)), SimpleParts_HybridFitness ["entropy"])
ax1.plot(range(len(DoubleParts_HybridFitness)), DoubleParts_HybridFitness ["entropy"])
ax1.plot(range(len(TripleParts_HybridFitness)), TripleParts_HybridFitness ["entropy"])

ax1.set_xlabel('generations')
ax1.set_ylabel('Shannon entropy')
ax1.set_title('Shannon entropy')
ax1.grid(True)

# num logic functions on the right
ax2.plot(range(len(SimpleParts_EntropyFitness)), SimpleParts_EntropyFitness["fun_count"])
ax2.plot(range(len(SimpleParts_NumFunsFitness)), SimpleParts_NumFunsFitness["fun_count"])
ax2.plot(range(len(SimpleParts_HybridFitness)), SimpleParts_HybridFitness["fun_count"])
ax2.plot(range(len(DoubleParts_HybridFitness)), DoubleParts_HybridFitness["fun_count"])
ax2.plot(range(len(TripleParts_HybridFitness)), TripleParts_HybridFitness["fun_count"])



ax2.set_xlabel('generations')
ax2.set_ylabel('Number of unique logic functions')
ax2.set_title('Logic function count')
ax2.grid(True)


# Adjust spacing between subplots
plt.subplots_adjust(wspace=0.4)


plt.savefig(PATH + line_name)
# plt.show()


## plot bar plot showing function distribution of final best of gen ##

best_fun_dist_0 = ast.literal_eval(SimpleParts_EntropyFitness.iloc[-1]["fun_dist"])
best_fun_dist_1 = ast.literal_eval(SimpleParts_NumFunsFitness.iloc[-1]["fun_dist"])
best_fun_dist_2 = ast.literal_eval(SimpleParts_HybridFitness.iloc[-1]["fun_dist"])
best_fun_dist_3 = ast.literal_eval(DoubleParts_HybridFitness.iloc[-1]["fun_dist"])
best_fun_dist_4 = ast.literal_eval(TripleParts_HybridFitness.iloc[-1]["fun_dist"])





labels = list(function_names.keys())
plt.style.use('seaborn-colorblind')
fig, axs = plt.subplots(5, 1, figsize=(8, 10))

axs[0].bar(labels, best_fun_dist_1)
# axs[0].set_xticks(range(0, len(labels)))
axs[0].set_xticklabels(labels, rotation=90)
axs[0].set_ylabel('Counts')
axs[0].set_ylim(0,729)

axs[1].bar(labels, best_fun_dist_1)
axs[2].bar(labels, best_fun_dist_2)
axs[3].bar(labels, best_fun_dist_3)
axs[4].bar(labels, best_fun_dist_1)

plt.subplots_adjust(bottom=0.2)  # Adjust the bottom margin

plt.savefig(PATH + bar_name)
plt.show()