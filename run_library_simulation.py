import simlib_evo_v2 as sl
import matplotlib.pyplot as plt



### part_sets: this is the input 
part_set_a, part_set_b, part_set_c = ['pTet', 'T10'], ['pBAD', 'pPsrA', 'pTac'], ['AraC', 'PsrA', 'tfSp']
 
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
print('library length', len(library))
print('library phenotype length', len(library_phenotype))
fitness = sl.logical_evolvability(library_phenotype)
print('library fitness', fitness)


### CREATE HISTOGRAM ###

### turn library_phenotype into list of strings
phenotype_str = []

for i in range(len(library_phenotype)):
    phenotype_str.append(''.join(str(e) for e in library_phenotype[i].values()))  

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
plt.ylim(0,324)
plt.subplots_adjust(bottom=0.19)
plt.show()






### single circuit test ###
# feedback_circuit = 'pTet-a_pBAD-b_AraC-c_pTet-a_pBAD-b_AraC-c'
# print(sl.simulate_circuit_function(feedback_circuit))