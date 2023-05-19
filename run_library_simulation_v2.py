import simlib_evo_v2 as sl
import matplotlib.pyplot as plt
import pandas as pd

PATH = "C:/Users/simca/Google_Drive/WORK/Phd_project/Experimental/Fun-Landscapes/Nanopore_seq/seq_pipeline/"

### part_sets: this is the input 

### part_set 1 ###
part_set_a, part_set_b, part_set_c = ['pTet', 'T10'], ['pBAD', 'pPsrA', 'pTac'], ['AraC', 'PsrA', 'tfSp']

### best 3x3 part set cound by GA so far ###

# part_set_a, part_set_b, part_set_c =  ['pBM3R1_BM3R1', 'pTet_PsrA', 'pTac_AraC'], ['PhIF_BetI', 'pTet_BM3R1', 'BM3R1_LmrA'], ['pPhIF_pPsrA', 'PhIF_BetI', 'pTet_pBM3R1']
# part_set_a, part_set_b, part_set_c = ['BM3R1_LmrA', 'pPhIF_PhIF', 'pTac_PhIF'], ['pBAD_pPhIF', 'pTet_PhIF', 'pTra*_pBM3R1'], ['pLmrA_TraR(W)', 'pTet_BM3R1', 'pPhIF_TraR(W)']

# ### CELLO EQUALS SET ####
# part_set_a, part_set_b, part_set_c = ['pTac_pHlyIIR', 'pTet_pHlyIIR_BetI'], ['PhIF_T10_pPhIF', 'T10_pTac_pTet'], ['pBetI_BM3R1_T10', 'HlyIIR_T10_pBM3R1']




 
function_names = {
'FALSE': '[0][0][0][0]',
'AND': '[0][0][0][1]',
'A_ANDN_B': '[0][0][1][0]',
'A': '[0][0][1][1]',
'B_ANDN_A': '[0][1][0][0]',
'B': '[0][1][0][1]',
'XOR': '[0][1][1][0]',
'OR' : '[0][1][1][1]',
'NOR' : '[1][0][0][0]',
'EQUALS': '[1][0][0][1]',
'NOT_B': '[1][0][1][0]',
'A_ORN_B': '[1][0][1][1]',
'NOT_A': '[1][1][0][0]',
'B_ORN_A': '[1][1][0][1]',
'NAND': '[1][1][1][0]',
'TRUE': '[1][1][1][1]',
'CYCLIC': None
}


library = sl.library_generator(part_set_a, part_set_b, part_set_c)
library_phenotype = sl.simulate_library_phenotype(library)
print("library phenotype", library_phenotype)
print('library length', len(library))
# print(library)
print('library phenotype length', len(library_phenotype))
fitness = sl.logical_evolvability(library_phenotype)
print('library fitness', fitness)


### compress logic gates with internal attractors (i.e. repeated attractors on the output), into point attractors
logics_with_internal_attractors = []
for i in range(len(library_phenotype)):
    logics_with_internal_attractors.append([set(i) for i in library_phenotype[i].values()])    ### make repeated attractor states into single-state e.g. [[0], [1], [0,0], [1,1]] becomes [{0}, {1}, {0}, {1}]    

### turn library_phenotype into list of strings
phenotype_str = []   
for i in range(len(library_phenotype)):         
    phenotype_str.append(''.join(str(e) for e in logics_with_internal_attractors[i]))

print(phenotype_str[0])

for i in range(len(phenotype_str)): 
    phenotype_str[i] = phenotype_str[i].replace("{", "[")
    phenotype_str[i] = phenotype_str[i].replace("}", "]")


print("phenotype_str: ", phenotype_str)


### save library phenotype to csv ###
library_phenotype_df = pd.DataFrame(zip(library, phenotype_str), columns=["construct_name", "function"])
print(library_phenotype_df)
library_phenotype_df.to_csv(PATH+"library_phenotype_internal_oscillators_included.csv", header=True, mode="w")


### true_logics are those with only point attractors
true_logics = [x for x in phenotype_str if len(x) == 12]
cyclic_functions = [x for x in phenotype_str if len(x) > 12]

### create a list of frequencies of each logic function, in the order seen in the dict.
logic_function_counts = []
for key in function_names:
    logic_function_counts.append(true_logics.count(function_names[key]))

### add the count of cyclic functions
logic_function_counts[-1] = len(cyclic_functions)

print('logic function counts', logic_function_counts)


### PLOTTING ###



x_labels = list(function_names.keys())
plt.bar(range(len(logic_function_counts)), logic_function_counts, tick_label=x_labels)
plt.xticks(fontsize=9, rotation=90)
plt.ylim(0,100)
plt.subplots_adjust(bottom=0.19)
plt.show()






### single circuit test ###
# feedback_circuit = 'pTet-a_pBAD-b_AraC-c_pTet-a_pBAD-b_AraC-c'
# print(sl.simulate_circuit_function(feedback_circuit))