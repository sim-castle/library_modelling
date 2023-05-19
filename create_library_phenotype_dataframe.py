import simlib_evo_v2 as sl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

PATH = "C:/Users/simca/Google_Drive/WORK/Phd_project/Experimental/Fun-Landscapes/Nanopore_seq/seq_pipeline/"

### part_sets: this is the input 

### part_set 1 ###
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


# def simulate_library_full_phenotype(library, simulate_circuit_function=simulate_circuit_function, part_catalogue=part_catalogue):
#     output_list = []

#     for construct in range(len(library)):
#         circuit_str = library[construct]
#         ### use this block for writing to list (fast)
#         phenotype = simulate_circuit_function(circuit_str)
#         output_list.append(phenotype)

library = sl.library_generator(part_set_a, part_set_b, part_set_c)
phenotype = sl.simulate_library_full_phenotype(library)

phenotype_transposed = []
for construct in phenotype:
    phenotype_1_state_transposed = []
    for state in construct:      
        phenotype_1_state_transposed.append(np.array(state).T.tolist())
    phenotype_transposed.append(phenotype_1_state_transposed)

### split the construct names into the library into lists rather than single strings
library = [name.split("_") for name in library] 
library_df = pd.DataFrame(library, columns = ["part0", "part1", "part2", "part2", "part4", "part5"])

phenotype_df = pd.DataFrame(phenotype_transposed, columns = ["-/-", "-/+", "+/-", "+/+"])

phenotype_df["output_phenotype"] = phenotype_df["-/-"][]


results_df = pd.concat([library_df, phenotype_df], axis=1)

### add column with output phenotypes
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


results_df.to_csv("library_full_df.csv")

