# Algoritmos Genéticos - UCA
# la ecuación que vamos a implementar.

# Y = w1x1 + w2x2 + w3x3 + w4x4 + w5x5 + w6x6

# La ecuación tiene 6 entradas (x1 a x6) y 6 pesos (w1 a w6) como se muestra.
# Los valores de las entradas son (x1, x2, x3, x4, x5, x6) = (4,-2,7,5,11, 1).
# Estamos buscando encontrar los parámetros (pesos) que maximicen dicha ecuación.
# La idea de maximizar tal ecuación parece simple.
# La entrada positiva se multiplicará por el número positivo más grande posible y
# el número negativo se multiplicará por el número negativo más pequeño posible.
# Pero la idea que estamos buscando implementar es cómo hacer que GA haga eso por su cuenta
# para saber que es mejor usar el peso positivo con entradas positivas y los pesos negativos con entradas negativas.

import numpy
import ga

#Al principio, creemos una lista de las 6 entradas y una variable para contener el número de pesos de la siguiente manera:

equation_inputs = [4,-2,3.5,5,-11,-4.7]
# cantidad factores o pesos a optimizar
num_weights = 6

# El siguiente paso es definir la población inicial.
# Según el número de pesos, cada cromosoma (solución o individuo) en la población definitivamente tendrá 6 genes,
# un gen para cada peso. Pero la pregunta es ¿cuántas soluciones por población?
# No hay un valor fijo para eso y podemos seleccionar el valor que se ajuste bien a nuestro problema.
# Pero podríamos dejarlo genérico para que se pueda cambiar en el código.
# A continuación, creamos una variable que contiene el número de soluciones por población,
# otra para contener el tamaño de la población y, finalmente, una variable que contiene la población inicial real:

sol_per_pop = 20

# Definimos el tamaño de la población.MAXIMIZE REGRESION

pop_size = (sol_per_pop,num_weights)
# La población tendrá un cromosoma sol_per_pop donde cada cromosoma tiene genes con peso num_weights.
# Crear la población inicial.

new_population = numpy.random.uniform(low=-4.0, high=4.0, size=pop_size)
print("Poblacion Inicial\n",new_population)
# Después de importar la biblioteca numpy, podemos crear la población inicial al azar
# utilizando la función numpy.random.uniform.
# De acuerdo con los parámetros seleccionados, tendrá forma (8, 6).
# Eso es 8 cromosomas y cada uno tiene 6 genes, uno para cada peso.
# Después de ejecutar este código, la población es la siguiente:

# [[-2.19134006 -2.88907857  2.02365737 -3.97346034  3.45160502  2.05773249]
# [ 2.12480298  2.97122243  3.60375452  3.78571392  0.28776565  3.5170347 ]
# [ 1.81098962  0.35130155  1.03049548 -0.33163294  3.52586421  2.53845644]
# [-0.63698911 -2.8638447   2.93392615 -1.40103767 -1.20313655  0.30567304]
# [-1.48998583 -1.53845766  1.11905299 -3.67541087  1.33225142  2.86073836]
# [ 1.14159503  2.88160332  1.74877772 -3.45854293  0.96125878  2.99178241]
# [ 1.96561297  0.51030292  0.52852716 -1.56909315 -2.35855588  2.29682254]
# [ 3.00912373 -2.745417    3.27131287 -0.72163167  0.7516408   0.00677938]]

# Tener en cuenta que se genera aleatoriamente y, por lo tanto, definitivamente cambiará cuando se ejecute nuevamente.
# Después de preparar a la población, lo siguiente es seguir el diagrama de flujo del AG.
# Según la función de aptitud física, vamos a seleccionar a los mejores individuos de la población actual como padres
# para el apareamiento. Lo siguiente es aplicar las variantes de GA (cruce y mutación) para producir la descendencia
# de la próxima generación, creando la nueva población agregando padres y descendientes, y repitiendo estos pasos
# para una serie de iteraciones / generaciones. El siguiente código aplica estos pasos:

num_generations = 100

num_parents_mating = 4
for generation in range(num_generations):
    # Medición de la aptitud de cada cromosoma en la población.
    fitness = ga.cal_pop_fitness(equation_inputs, new_population)
    print("Generación=", generation+1, "\nAptitud\n",fitness)
    # Selección de los mejores padres de la población para el apareamiento.
    parents = ga.select_mating_pool(new_population, fitness,
                                    num_parents_mating)
    print("Selección de padres: \n",parents)

    # Generando la próxima generación usando cruza.
    offspring_crossover = ga.crossover(parents, offspring_size=(pop_size[0] - parents.shape[0], num_weights))
    print("Cruza\n",offspring_crossover)

    # Agregar algunas variaciones a la descendencia usando la mutación.
    offspring_mutation = ga.mutation(
        offspring_crossover)
    print(offspring_crossover)
    print("Mutación\n",offspring_mutation)
    # Crear la nueva población basada en los padres y la descendencia.
    new_population[0:parents.shape[0], :] = parents
    new_population[parents.shape[0]:, :] = offspring_mutation
    print("Poblacion Evolucionada\n", new_population)
    print("MEJOR RESULTADO PARA ESTA GENERACION : ", numpy.max(numpy.sum(new_population*equation_inputs, axis=1)))
fitness = ga.cal_pop_fitness(equation_inputs, new_population)

# Indice de la solución para la mejor aptitud
best_match_idx = numpy.where(fitness == numpy.max(fitness))

print("MEJOR SOLUCION: ", new_population[best_match_idx, :])
print("MEJOR APTITUD : ", fitness[best_match_idx])


# El número actual de generaciones es 5. Se selecciona para ser pequeño para presentar resultados de todas las
# generaciones dentro del tutorial. Hay un módulo llamado GA que contiene la implementación del algoritmo.
# El primer paso es encontrar el valor de aptitud de cada solución dentro de la población utilizando
# la función ga.cal_pop_fitness. La implementación de dicha función dentro del módulo GA es la siguiente:

def cal_pop_fitness(equation_inputs, pop):
    # Cálculo del valor de aptitud de cada solución en la población actual.
    # La función fitness calcula la suma de productos entre cada entrada y su peso correspondiente.
    fitness = numpy.sum(pop * equation_inputs, axis=1)
    print("-----------------------------\n",pop,equation_inputs,fitness)
    return fitness

# La función de aptitud acepta los valores de entrada de ecuación (x1 a x6) además de la población.
# El valor de aptitud se calcula como la suma del producto (SOP) entre cada entrada y su gen correspondiente (peso)
# de acuerdo con nuestra función. Según el número de soluciones por población, habrá una serie de POE.
# Como establecimos previamente el número de soluciones en 8 en la variable llamada sol_per_pop, habrá 8 SOP
# como se muestra a continuación:
# [-63.41070188  14.40299221 -42.22532674  18.24112489 -45.44363278 -37.00404311  15.99527402  17.0688537 ]

# Tenga en cuenta que cuanto mayor sea el valor de aptitud, mejor será la solución.
# Después de calcular los valores de aptitud para todas las soluciones, a continuación se selecciona
# la mejor de ellas como padres en el grupo de apareamiento de acuerdo con la siguiente función ga.select_mating_pool.
# Dicha función acepta la población, los valores de condición física y la cantidad de padres necesarios.
# Devuelve los padres seleccionados. Su implementación dentro del módulo GA es la siguiente:

def select_mating_pool(pop, fitness, num_parents):
    # Seleccionar a los mejores individuos de la generación actual como padres para producir
    # la descendencia de la próxima generación.

    parents = numpy.empty((num_parents, pop.shape[1]))

    for parent_num in range(num_parents):
        max_fitness_idx = numpy.where(fitness == numpy.max(fitness))
        max_fitness_idx = max_fitness_idx[0][0]
        parents[parent_num, :] = pop[max_fitness_idx, :]
        fitness[max_fitness_idx] = -99999999999
    return parents


# Según la cantidad de padres necesarios según se define en la variable num_parents_mating, la función crea
# una matriz vacía para mantenerlos como en esta línea:
# parents = numpy.empty ((num_parents, pop.shape [1]))

# Recorriendo la población actual, la función obtiene el índice del valor de condición de aptitud más alto
# porque es la mejor solución para seleccionar de acuerdo con esta línea:

max_fitness_idx = numpy.where(fitness == numpy.max(fitness))

# Este índice se utiliza para recuperar la solución que corresponde a dicho valor de aptitud utilizando esta línea:

# parents [parent_num,:] = pop [max_fitness_idx,:]

# Para evitar seleccionar nuevamente dicha solución, su valor de aptitud se establece en un valor muy pequeño
# que probablemente no se volverá a seleccionar, que es -99999999999.
# Finalmente, se devuelve la matriz de parents, que será la siguiente según nuestro ejemplo:

# [[-0.63698911 -2.8638447   2.93392615 -1.40103767 -1.20313655  0.30567304]
# [ 3.00912373 -2.745417    3.27131287 -0.72163167  0.7516408   0.00677938]
# [ 1.96561297  0.51030292  0.52852716 -1.56909315 -2.35855588  2.29682254]
# [ 2.12480298  2.97122243  3.60375452  3.78571392  0.28776565  3.5170347 ]]


# Tenga en cuenta que estos padres son los mejores individuos dentro de la población actual en función de
# sus valores de función de aptitud que son 18.24112489, 17.0688537, 15.99527402 y 14.40299221, respectivamente.

# El siguiente paso es utilizar dichos padres seleccionados para el apareamiento con el fin de generar la descendencia.
# El apareamiento comienza con la operación de cruce de acuerdo con la función ga.crossover.
# Esta función acepta los padres y el tamaño de la descendencia.
# Utiliza el tamaño de la descendencia para saber la cantidad de descendencia que se producirá de dichos padres.
# Dicha función se implementa de la siguiente manera dentro del módulo GA:

def crossover(parents, offspring_size):
    offspring = numpy.empty(offspring_size)
    # El punto en el que se produce el cruce entre dos padres.
    # Por lo general, está en el centro.
    crossover_point = numpy.uint8(offspring_size[1] / 2)

    for k in range(offspring_size[0]):
        # Índice del primer progenitor en aparearse.
        parent1_idx = k % parents.shape[0]
        # Índice del segundo progenitor en aparearse.
        parent2_idx = (k + 1) % parents.shape[0]
        # La nueva descendencia tendrá su primera mitad de sus genes tomados del primer progenitor.
        offspring[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]
        # La nueva descendencia tendrá su segunda mitad de sus genes tomados del segundo progenitor.
        offspring[k, crossover_point:] = parents[parent2_idx, crossover_point:]
    return offspring

# La función comienza creando una matriz vacía basada en el tamaño de la descendencia como en esta línea:

# offspring = numpy.empty (tamaño de la descendencia)

# Debido a que estamos utilizando el cruce de un solo punto, debemos especificar el punto en el que tiene lugar el cruce.
# El punto se selecciona para dividir la solución en dos mitades iguales de acuerdo con esta línea:

# crossover_point = numpy.uint8 (offspring_size [1] / 2)

# Luego tenemos que seleccionar a los dos padres para cruzar.
# Los índices de estos padres se seleccionan de acuerdo con estas dos líneas:

# parent1_idx = k% parents.shape [0]
# parent2_idx = (k + 1)% parents.shape [0]

# Los padres se seleccionan de manera similar a un anillo. Los primeros con los índices 0 y 1 se seleccionan
# al principio para producir dos descendientes. Si todavía queda descendencia para producir,
# entonces seleccionamos el padre 1 con el padre 2 para producir otras dos crías.
# Si necesitamos más descendientes, seleccionamos los siguientes dos padres con los índices 2 y 3.
# Por el índice 3, llegamos al último padre. Si necesitamos producir más descendientes,
# seleccionamos el padre con el índice 3 y volvemos al padre con el índice 0, y así sucesivamente.

# Las soluciones después de aplicar la operación de cruce a los padres se almacenan
# en la variable offspring (descendencia) y son las siguientes:
# [[-0,63698911 -2,8638447 2,93392615 0,00677938 0,7516408 -0,72163167]
# [3,00912373 3,27131287 -2,745417 -1,56909315 -2,35855588 2,29682254]
# [0,51030292 0,52852716 3,78571392 1,96561297 0,28776565 3,5170347]
# [2,12480298 2,97122243 3,60375452 0,30567304 -1,40103767 -1,20313655]]

# Lo siguiente es aplicar la segunda variante de GA, mutación, a los resultados del cruce almacenado en la
# variable offspring utilizando la función ga.mutation dentro del módulo GA.
# Dicha función acepta la descendencia cruzada y la devuelve después de aplicar una mutación uniforme.
# Esa función se implementa de la siguiente manera:

def mutation(offspring_crossover):
    # La mutación cambia un solo gen en cada descendencia al azar.
    for idx in range(offspring_crossover.shape[0]):
        # El valor aleatorio que se agregará al gen.
        random_value = numpy.random.uniform(-1.0, 1.0, 1)
        offspring_crossover[idx, 4] = offspring_crossover[idx, 4] + random_value
    return offspring_crossover

# Recorre cada descendencia y agrega un número aleatorio generado uniformemente en el rango de -1 a 1 de acuerdo
# con esta línea:

# random_value = numpy.random.uniform (-1.0, 1.0, 1)

# Dicho número aleatorio se agrega al gen con el índice 4 de la descendencia de acuerdo con esta línea:

# offspring_crossover [idx, 4] = offspring_crossover [idx, 4] + valor_aleatorio

# Tenga en cuenta que el índice podría cambiarse a cualquier otro índice. Los descendientes después de aplicar
# la mutación son los siguientes:
# [[-0,63698911 -2,8638447 2,93392615 1,66083721 0,00677938 -0,72163167]
# [3,00912373 3,27131287 -2,745417 -1,56909315 -1,94513681 2,29682254]
# [0,51030292 0,52852716 3,78571392 1,96561297 0,45337472 3,5170347]
# [2,12480298 2,97122243 3,60375452 0,30567304 -1,40103767 -1,5781162]]

# Dichos resultados se agregan a la variable offspring_crossover y la función los devuelve.
# En este punto, producimos con éxito 4 descendientes de los 4 padres seleccionados y estamos listos para crear
# la nueva población de la próxima generación.

# Tenga en cuenta que GA es una técnica de optimización basada en el azar.
# Intenta mejorar las soluciones actuales mediante la aplicación de algunos cambios aleatorios.
# Debido a que tales cambios son aleatorios, no estamos seguros de que produzcan mejores soluciones.
# Por tal razón, se prefiere mantener las mejores soluciones anteriores (padres) en la nueva población.
# En el peor de los casos, cuando todos los nuevos descendientes sean peores que dichos padres,
# continuaremos utilizando dichos padres. Como resultado, garantizamos que la nueva generación al menos conservará
# los buenos resultados anteriores y no empeorará.
# La nueva población tendrá sus primeras 4 soluciones de los padres anteriores. Las últimas 4 soluciones provienen
# de la descendencia creada después de aplicar el crossover y la mutación:

# new_population [0: parents.shape [0],:] = parents
# new_population [parents.shape [0] :,:] = offspring_mutation

# Al calcular la idoneidad de todas las soluciones (padres e hijos) de la primera generación,
# su idoneidad es la siguiente:

# [18.24112489 17.0688537 15.99527402 14.40299221 -8.46075629 31.73289712 6.10307563 24.08733441]

# El estado físico más alto anteriormente era 18.24112489, pero ahora es 31.7328971158.
# Eso significa que los cambios aleatorios se movieron hacia una mejor solución. Esto es genial.
# Pero tales resultados podrían mejorarse al pasar por más generaciones.
# A continuación se muestran los resultados de cada paso para otras 4 generaciones:

# Generación 1:
# Aptitud: [18.24112489 17.0688537 15.99527402 14.40299221 -8.46075629 31.73289712 6.10307563 24,08733441]
# padres seleccionados: [[3.00912373 -2.745417 3,27131287 2,29682254 -1.56909315 -1.94513681]
# [2,12480298 2,97122243 3,60375452 -1.40103767 -1.5781162 0.30567304]
# [- 0,63698911 2,93392615 -2.8638447 -1.40103767 - 1.20313655 0.30567304]
# [3,00912373 3,27131287 -2,745417 -0,72163167 0,7516408 0,00677938]]
# resultado Crossover: [[3,00912373 3,27131287 -2,745417 -1,40103767 -1,5781162 0,30567304]
# [2,12480298 2,97122243 3,60375452 0,30567304 -1,40103767 -1,20313655]
# [- 0,63698911 2,93392615 -2,8638447 -0,72163167 0,7516408 0,00677938]
# [3,00912373 3,27131287 -2,745417 -1,56909315 -1,94513681 2,29682254]]
# resultado mutación: [[3,00912373 3,27131287 -2,745417 -1,40103767 -1,2392086 0,30567304]
# [2,12480298 2,97122243 3,60375452 0,30567304 -1,40103767 -0,38610586]
# [- 0,63698911 2,93392615 -2,8638447 -0,72163167 1,33639943 0,00677938]
# [3,009 12373 -2.745417 3,27131287 -1,56909315 -1,13941727 2.29682254]]
# Mejor resultado después de la generación 1:
# Padres [31,73289712 24,08733441 18,24112489 34,16636692 10,97522073 17.0688537 -4,89194068 22,86998223]
# seleccionados:: valores 2Fitness: 34.1663669207
# Generación 2 [[3,00912373 3,27131287 -2,745417 -1,40103767 -1,2392086 0.30567304]
# [ 3,00912373 3,27131287 -2,745417 -1,56909315 -1,94513681 2,29682254]
# [2,12480298 2,97122243 3,60375452 0,30567304 -1,40103767 -1,5781162]
# [3,00912373 3,27131287 -2,745417 -1,56909315 -1,13941727 2,29682254]]
# resultado Crossover: [[3,00912373 3,27131287 -2,745417 -1,56909315 -1,94513681 2,29682254]
# [3,00912373 - 2.745417 3,27131287 0,30567304 -1,40103767 -1,5781162]
# [2,12480298 2,97122243 3,60375452 2,29682254 -1,56909315 -1,13941727]
# [3,00912373 3,27131287 -2,745417 -1,40103767 -1,2392086 0,30567304]]
# resultado mutación: [[3,00912373 3,27131287 -2,745417 -1,56909315 -2,20515009 2,29682254]
# [3,00912373 3,27131287 -2,745417 -1 .40103767 -0,73543721 0,30567304]
# [2,12480298 2,97122243 3,60375452 2,29682254 -1,56909315 -0,50581509]
# [3,00912373 3,27131287 -2,745417 -1,40103767 -1,20089639 0,30567304]]
# Mejor resultado después de la generación 2: valores 3cFitness:: 34.5930432629
# Generation 3 [34,16636692 31,73289712 24,08733441 22,86998223 34,59304326 2,09334217 28.6248816 33.7449326]
# padres seleccionados: [[3,00912373 3,27131287 -2.745417 -1.56909315 -2.20515009 2.29682254]
# [3,00912373 3,27131287 -2.745417 -1.40103767 -1.2392086 0.30567304]
# [3,00912373 3,27131287 -2.745417 -1.40103767 -1.20089639 0.30567304]
# [3,00912373 3,27131287 -2.745417 -1.56909315 -1.94513681 2.29682254]]
# Crossover resultados: [[3,00912373 3,27131287 -2,745417 -1,40103767 -1,2392086 0,30567304]
# [3,00912373 3,27131287 -2,745417 -1,40103767 -1,20089639 0,30567304]
# [3,00912373 3,27131287 -2,745417 -1,56909315 -1,94513681 2,29682254]
# [3,00912373 3,27131287 -2,745417 -1,56909315 -2,20515009 2,29682254]]
# resultado mutación : [[3,00912373 3,27131287 -2,745417 -1,40103767 -2,20744102 0,30567304]
# [3,00912373 3,27131287 -2,745417 -1,40103767 -1,16589294 0,30567304]
# [3,00912373 3,27131287 -2,745417 -1,56909315 -2,37553107 2,29682254]
# [3,00912373 3,27131287 -2,745417 -1,56909315 -2,44124005 2,29682254]]
# Mejor resultado después de la generación 3: valores 4
# Fitness [34.59304326 34,16636692 33,7449326 31,73289712 44.8169235233.35989464 36,46723397 37,19003273]
# padres seleccionados:: 44.8169235189
# Generation 4 [[3.00912373 -2.745417 3,27131287 0,30567304 -1.40103767 -2.20744102]
# [3.00912373 -2.745417 3,27131287 2,29682254 -1.56909315 -2.44124005]
# [3.00912373 3.27131287 -2.745417 - 1.56909315 2.29682254 -2,37553107]
# [3,00912373 3,27131287 -2,745417 -1,56909315 -2,20515009 2,29682254]]
# resultado Crossover: [[3,00912373 3,27131287 -2,745417 -1,56909315 -2,37553107 2,29682254]
# [3,00912373 3,27131287 -2,745417 -1,56909315 -2,20515009 2,29682254]
# [3,00912373 3,27131287 -2,745417 -1,40103767 -2,2 0744102 0.30567304]]
# resultado Mutación: [[3,00912373 3,27131287 -2,745417 -1,56909315 -2,13382082 2,29682254]
# [3,00912373 3,27131287 -2,745417 -1,56909315 -2,98105233 2,29682254]
# [3,00912373 3,27131287 -2,745417 -1,56909315 -2,27638584 2,29682254]
# [3,00912373 3,27131287 -2,745417 -1,40103767 -1,70558545 0.30567304]]
# Mejor resultado después de la generación 4: 44.8169235189

# Después de las 5 generaciones anteriores, el mejor resultado ahora tiene un valor de aptitud igual a 44.8169235189
# en comparación con el mejor resultado después de la primera generación, que es 18.24112489.

# La mejor solución tiene los siguientes pesos:
# [3.00912373 -2.745417 3.27131287 -1.40103767 -2.20744102 0.30567304]

