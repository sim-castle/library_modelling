### 100 random function landscapes from part-catalogue ###

import simlib_evo_v2 as sl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import entropy



def create_df_from_phenotype(library, phenotype):
	phenotype_transposed = []
	for construct in phenotype:
	    phenotype_1_state_transposed = []
	    for state in construct:      
	        phenotype_1_state_transposed.append(np.array(state).T.tolist())
	    phenotype_transposed.append(phenotype_1_state_transposed)

	### split the construct names into the library into lists rather than single strings
	library = [name.split("_") for name in library] 
	library_df = pd.DataFrame(library, columns = ["part0", "part1", "part2", "part3", "part4", "part5"])

	phenotype_df = pd.DataFrame(phenotype_transposed, columns = ["-/-", "-/+", "+/-", "+/+"])


	results_df = pd.concat([library_df, phenotype_df], axis=1)

	### add column with output phenotypes ####
	minusminus = [i[-1] for i in phenotype_df["-/-"]]
	minusplus = [i[-1] for i in phenotype_df["-/+"]]
	plusminus = [i[-1] for i in phenotype_df["+/-"]]
	plusplus = [i[-1] for i in phenotype_df["+/+"]]

	output_phenotype = list(zip(minusminus,minusplus,plusminus,plusplus))

	### output phenotypes are compressed for repeated output attractors
	for j, construct in enumerate(output_phenotype):
	    output_phenotype[j] = list( output_phenotype[j])
	    for i,x in enumerate( output_phenotype[j]):
	        if x[0] == x[-1]:
	            output_phenotype[j][i] = [x[-1]]

	results_df["output_phenotype"] = output_phenotype
	return results_df

pop_size = 100
PATH = "C:/Users/simca/Google_Drive/WORK/Phd_project/Experimental/Fun-Landscapes/Library_Modelling/library_simulator/100_random_fun_landscapes_output/"
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


## generate set of random part-set function distributions
distributions = []
for ind in range(pop_size):

	### create random part_sets
	rand_genome = sl.create_rand_genome(part_catalogue=sl.part_catalogue, length=9)
	part_sets = sl.genome_to_part_sets(rand_genome)

	### create a library and phenotype
	library = sl.library_generator(part_sets[0], part_sets[1], part_sets[2])
	phenotype = sl.simulate_library_full_phenotype(library)

	### save results
	results_df = create_df_from_phenotype(library, phenotype)
	# print(results_df["output_phenotype"])
	results_df.to_csv(PATH+"rand_fun_landscape_{}.csv".format(ind))

	# print("output phenotype list:", list(results_df["output_phenotype"]))

	### calculate distribution
	### create a list of frequencies of each logic function, in the order seen in the dict.
	logic_function_counts = []
	for key in function_names:
			logic_function_counts.append(list(results_df["output_phenotype"]).count(function_names[key]))

	cyclic_funs_count = len(results_df) - sum(logic_function_counts)
	logic_function_counts[-1] = cyclic_funs_count

	print("counts {}".format(ind), logic_function_counts)

	distributions.append(logic_function_counts)


### Summary stats 
distributions_df = pd.DataFrame(distributions) 
print()
print("distributions dataframe", distributions_df)
print()

### normalise count values to 1
### xxxxxx TO DO #####

### mean of aggregate distributions
mean_freqs = []
std_devs = []
for column in distributions_df.columns:
	mean_freqs.append(np.mean(distributions_df[column]))
	std_devs.append(np.std(distributions_df[column]))

print("means:", mean_freqs)
print("std devs:", std_devs)

### mean number of unique functions 
unique_logic_funs = []
for index, row in distributions_df.iterrows():
	unique_logic_funs.append(len([num for num in row[0:-1] if num != 0]))

print()
print("unique_logic_funs:", unique_logic_funs)

mean_unique_funs = np.mean(unique_logic_funs)
std_dev_unique_funs = np.std(unique_logic_funs)

print("mean unique logic functions:", mean_unique_funs)
print("std dev unique logic functions", std_dev_unique_funs)

### entropy calculations
shannon_entropies = []
for index, row in distributions_df.iterrows():
	shannon_entropies.append(entropy(row, base=2))

mean_shannon_entropy = np.mean(shannon_entropies)
std_shannon_entropy = np.std(shannon_entropies)

print("mean shannon_entropies", mean_shannon_entropy)
print("std_shannon_entropies", std_shannon_entropy)

### plot aggregate distribution

# Set x-axis labels
labels = list(function_names.keys())
plt.style.use('seaborn-colorblind')
fig, ax = plt.subplots()
ax.violinplot(distributions_df.values, showmedians=True)

ax.set_xticks(range(1, len(labels) + 1))
ax.set_xticklabels(labels, rotation=90)

ax.set_ylabel('Counts')
# ax.set_ylim(0,1)
ax.set_title('Aggregate distribution of functions for 100 randomly generated Combinatorial Assembly Schemes')
ax.grid(True)


plt.subplots_adjust(bottom=0.2)  # Adjust the bottom margin

# Add mean values to the plot
for i, col in enumerate(distributions_df.columns):
    mean_val = distributions_df[col].mean()
    ax.annotate(f'{mean_val:.4f}', xy=(i + 1, mean_val), xytext=(0, 25),
                textcoords='offset points', ha='center', va='top')


plt.show()





