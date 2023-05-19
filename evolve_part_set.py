import simlib_evo_v2 as sl



### setup
max_gens = 10
pop_size = 10
output_folder = 'output_1'
mutation_probability = 0.05										### ref: Choosing Mutation and Crossover Ratios for Genetic Algorithms—A Review with a New Dynamic Approach
crossover_probability = 0.8



toolbox = sl.setup_toolbox(genome_length=9)
print('line 27 done')

### initial generation
pop = toolbox.make_population(pop_size)
print('line 31 done')
sl.gp_map_pop(pop)
print('line 33 done')
sl.evaluate_pop(pop, evaluate_fun=sl.logical_evolvability)
print('line 36 done')
fitnesses = [pop[i].fitness.values for i in range(len(pop))]		### put fitnesses in a simple list view for printing to screen etc.
print('gen 0 fitness:', fitnesses)


print('initialisation complete')
print('starting evolution loop')
### beding evolution
gen_count = 0
best_of_gen = []

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
	sl.evaluate_pop(invalid_inds, evaluate_fun=sl.logical_evolvability)

	### Turnover population
	pop[:] = offspring	

	### save best individual of gen
	best_ind =  toolbox.selectBest(pop, 1)
	best_of_gen.append(best_ind)
	
	fits = [ind.fitness.values[0] for ind in pop]								## Gather all the fitnesses in one list
	print(best_of_gen[-1])
	print("  Max %s" % max(fits))
	print(max(fits))


print("-- End of (successful) evolution --")