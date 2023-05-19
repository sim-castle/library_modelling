import simlib_evo_v3 as sl
import matplotlib.pyplot as plt
import pandas as pd

PATH = "C:/Users/simca/Google_Drive/WORK/Phd_project/Experimental/Fun-Landscapes/Library_Modelling/library_simulator/GA_output/"


### setup
max_gens = 100
pop_size = 50
output_folder = 'output_1'
mutation_probability = 0.05										### ref: Choosing Mutation and Crossover Ratios for Genetic Algorithms—A Review with a New Dynamic Approach
crossover_probability = 0.8

best_of_gen = []
best_of_gen_phenotype = []
best_of_gen_fun_dist = []
best_of_gen_fun_count = []
best_of_gen_fitness = []
best_of_gen_entropies = []

toolbox = sl.setup_toolbox(genome_length=9)
print('line 27 done')

### initial generation
pop = toolbox.make_population(pop_size)
print('line 31 done')
sl.gp_map_pop(pop)
print('line 33 done')
sl.evaluate_pop(pop, evaluate_fun=sl.entropy_fitness)
print('line 36 done')
fitnesses = [pop[i].fitness.values for i in range(len(pop))]		### put fitnesses in a simple list view for printing to screen etc.
print('gen 0 fitness:', fitnesses)

############ save data of initial generation
best_ind =  toolbox.selectBest(pop, 1)
fits = [ind.fitness.values[0] for ind in pop]
best_of_gen.append(best_ind)

best_of_gen_phenotype.append(best_ind[0].phenotype)
fun_dist = sl.function_distribution(best_ind[0].phenotype)
best_of_gen_entropy = sl.entropy_fitness(best_ind[0].phenotype)[0]
best_of_gen_entropies.append(best_of_gen_entropy)
logic_fun_count = sl.num_logics(fun_dist) 
best_of_gen_fun_count.append(logic_fun_count)
best_of_gen_fun_dist.append(fun_dist)
best_of_gen_fitness.append(best_ind[0].fitness.values[0])
###########


print('initialisation complete')
print('starting evolution loop')
print('----------------------------')
### beding evolution
gen_count = 0



while gen_count < max_gens:
	gen_count +=1
	print('-- Generation %i --' % gen_count)	

	### Selection
	offspring = toolbox.select(pop, len(pop))									## selection of next gen

	### Reproduction
	offspring = list(map(toolbox.clone, offspring))								## Clone the selected individuals

	### Variation
	offspring = sl.mutate_pop(offspring, toolbox, MUTPB=mutation_probability)
	offspring = sl.crossover_pop(offspring, toolbox, CXPB=crossover_probability)

	### Production
	invalid_inds = sl.get_invalid_inds(offspring)
	sl.gp_map_pop(invalid_inds)

	### Evalution
	sl.evaluate_pop(invalid_inds, evaluate_fun=sl.entropy_fitness)

	### Turnover population
	pop[:] = offspring	

	### save best individual of gen
	best_ind =  toolbox.selectBest(pop, 1)
	best_of_gen.append(best_ind)

	fits = [ind.fitness.values[0] for ind in pop]

	best_of_gen_phenotype.append(best_ind[0].phenotype)
	fun_dist = sl.function_distribution(best_ind[0].phenotype)
	logic_fun_count = sl.num_logics(fun_dist) 
	best_of_gen_entropy = sl.entropy_fitness(best_ind[0].phenotype)[0]
	best_of_gen_entropies.append(best_of_gen_entropy)
	best_of_gen_fun_count.append(logic_fun_count)
	best_of_gen_fun_dist.append(fun_dist)
	best_of_gen_fitness.append(best_ind[0].fitness.values[0])
	


	print("best of gen genotype", best_of_gen[-1][0])
	# print("best of gen phenotype", best_of_gen[-1][0].phenotype)								## Gather all the fitnesses in one list
	print("best of gen function", sl.function_distribution(best_of_gen[-1][0].phenotype))
	print("best of gen fitness", best_of_gen[-1][0].fitness)
	# print("best of gen fitness %s" % max(fits))
	print(max(fits))
	print()

	print()


print("-- End of (successful) evolution --")

print("best of gens fun dists", best_of_gen_fun_dist)
print("best of bend fun counts", best_of_gen_fun_count)
print("best_of_gen_fitness", best_of_gen_fitness)


#### save output data
data = {
	"genotype": best_of_gen,
	"phenotype": best_of_gen_phenotype,
	"fun_dist": best_of_gen_fun_dist,
	"fun_count": best_of_gen_fun_count,
	"fitness":	best_of_gen_fitness, 
	"entropy": best_of_gen_entropies
}


output_df = pd.DataFrame(data)
output_df.to_csv(PATH + "GA_SimpleParts_EntropyFitness_gens100_pop50.csv", index=False)

# #### plotting ###

# ## plot 2 subplots, one for max shannon entropy v gens, one for max fun counts per gen
# # Create subplots
# plt.style.use('seaborn-colorblind')
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

# # shannon entropy plot on the left
# ax1.plot(range(len(best_of_gen)), best_of_gen_fitness)
# ax1.set_xlabel('generations')
# ax1.set_ylabel('Shannon entropy')
# ax1.set_title('Shannon entropy')
# ax1.grid(True)

# # num logic functions on the right
# ax2.plot(range(len(best_of_gen)), best_of_gen_fun_count)
# ax2.set_xlabel('generations')
# ax2.set_ylabel('Number of unique logic functions')
# ax2.set_title('Logic function count')
# ax2.grid(True)


# # Adjust spacing between subplots
# plt.subplots_adjust(wspace=0.4)


# plt.savefig(PATH + "simple_parts_entropy_fitness_shannon_counts.png")
# plt.show()