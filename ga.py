import numpy

def cal_pop_fitness(equation_inputs, pop):
    # Calculating the fitness value of each solution in the current population.
    # The fitness function caulcuates the sum of products between each input and its corresponding weight.
    fitness = numpy.sum(pop*equation_inputs, axis=1)
    #print("-----------------------------\n Población\n",pop,"\nValores de x\n",equation_inputs,"\nAptitud\n",fitness,"\n")
    return fitness

def cal_pop_fitness2(equation_inputs, pop):
    # Calculating the fitness value of each solution in the current population.
    # The fitness function calculates the sum of products between each input and its corresponding weight.
    fitness = numpy.sum(pop*equation_inputs, axis=1)-10
    print("-----------------------------\n Población\n",pop,"\nValores de x\n",equation_inputs,"\nAptitud\n",fitness,"\n")
    return fitness

def select_mating_pool(pop, fitness, num_parents):
    # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
    # pop.shape[1] 0 tamaño de la apoblación
    parents = numpy.empty((num_parents, pop.shape[1]))
    print("pop\n",pop.shape[1],num_parents)
    for parent_num in range(num_parents):
        fitness_idx = (numpy.abs(fitness-0)).argmin()
        print("fitness_idx",fitness_idx)
        a=fitness[fitness_idx]
        print(a)
        parents[parent_num, :] = pop[fitness_idx, :]
        fitness[fitness_idx] = -99999999999
    return parents

def crossover(parents, offspring_size):
    offspring = numpy.empty(offspring_size)
    # The point at which crossover takes place between two parents. Usually it is at the center.
    crossover_point = numpy.uint8(offspring_size[1]/2)

    for k in range(offspring_size[0]):
        # Index of the first parent to mate.
        parent1_idx = k%parents.shape[0]
        # Index of the second parent to mate.
        parent2_idx = (k+1)%parents.shape[0]
        # The new offspring will have its first half of its genes taken from the first parent.
        offspring[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]
        # The new offspring will have its second half of its genes taken from the second parent.
        offspring[k, crossover_point:] = parents[parent2_idx, crossover_point:]
    return offspring

def mutation(offspring_crossover):
    # Mutation changes a single gene in each offspring randomly.
    for idx in range(offspring_crossover.shape[0]):
        # The random value to be added to the gene.
        random_value = numpy.random.uniform(-1.0, 1.0, 1)
        offspring_crossover[idx, 2] = offspring_crossover[idx, 2] + random_value
    return offspring_crossover
