import numpy as np, random, operator, pandas as pd, matplotlib.pyplot as plt

"""
En el problema del Viajate de comercio, queremos buscar el trayecto mas corto
tal que recorramos las ciudades una vez en la menor distancia posible y 
volver al principio.

A continuación, definimos un modelo de la ciudad:
"""
class Ciudad:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distancia(self, ciudad):
        xDis = abs(self.x - ciudad.x)
        yDis = abs(self.y - ciudad.y)
        distancia = np.sqrt((xDis ** 2) + (yDis ** 2))
        return distancia

    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

"""
La aptitud es una métrica que utilizamos para comparar diferentes rutas
entre las ciudades. Cuanto mas grande es la aptitud (es decir, cuanto
mas chica es la distancia recorrida de la ruta), mejor es la ruta elegida.

En la clase definida a continuación primero se calcula la distancia de la
ruta y luego la aptitud se define como 1/distanciaDeLaRuta.
"""

class Aptitud:
    def __init__(self, ruta):
        self.ruta = ruta
        self.distancia = 0
        self.aptitud = 0.0

    def rutadistancia(self):
        if self.distancia == 0:
            caminodistancia = 0
            for i in range(0, len(self.ruta)):
                desdeCiudad = self.ruta[i]
                haciaCiudad = None
                if i + 1 < len(self.ruta):
                    haciaCiudad = self.ruta[i + 1]
                else:
                    haciaCiudad = self.ruta[0]
                caminodistancia += desdeCiudad.distancia(haciaCiudad)
            self.distancia = caminodistancia
        return self.distancia

    def rutaAptitud(self):
        if self.aptitud == 0:
            self.aptitud = 1 / float(self.rutadistancia())
        return self.aptitud

"""
crearRuta genera una ruta aleatoria apartir de las ciudades creadas.
Al fin al cabo, una ruta es un conjunto ordenado de ciudades.
"""

def crearRuta(ciudadList):
    ruta = random.sample(ciudadList, len(ciudadLista))
    print(ruta)
    return ruta

"""
La población inicial va a estar formada por un conjunto de rutas 
generadas con crearRuta().
"""

def poblacionInicial(tamPob, ciudadLista):
    poblacion = []

    for i in range(0, tamPob):
        poblacion.append(crearRuta(ciudadLista))
    return poblacion

"""
A partir de una población dada, se hace un ranking
de las aptitutes de cada uno de las rutas que 
conforman la misma.
"""

def rankingRutas(poblacion):
    aptitudResultados = {}
    for i in range(0,len(poblacion)):
        aptitudResultados[i] = Aptitud(poblacion[i]).rutaAptitud()
    return sorted(aptitudResultados.items(), key = operator.itemgetter(1), reverse = True)

"""
tamElite hace referencia a la cantidad de rutas que vamos a elegir
de las que mejor aptitud tienen (el Top 'tamElite'). De esta manera,
incluimos sí o sí a las mejores dentro de la selección. 

Luego, aleatoriamente y en función del percentil acumulado,
elegimos a las demas rutas a seleccionar.
"""

def seleccion(popRanqueada, tamElite):
    seleccionResultados = []
    df = pd.DataFrame(np.array(popRanqueada), columns=["Indice", "Aptitud"])
    df['cum_sum'] = df.Aptitud.cumsum()
    df['cum_perc'] = 100 * df.cum_sum / df.Aptitud.sum()

    for i in range(0, tamElite):
        print("i: ",i)
        seleccionResultados.append(popRanqueada[i][0])
    for i in range(0, len(popRanqueada) - tamElite):
        pick = 100 * random.random()
        for i in range(0, len(popRanqueada)):
            if pick <= df.iat[i, 3]:
                seleccionResultados.append(popRanqueada[i][0])
                break
    return seleccionResultados

"""
Luego de hacer la seleccion, pasamos a indicar quienes se van a aparear.
"""

def grupoApareamiento(poblacion, seleccionResultados):
    grupoapareamiento = []
    for i in range(0, len(seleccionResultados)):
        index = seleccionResultados[i]
        grupoapareamiento.append(poblacion[index])
    return grupoapareamiento

"""
Recibe dos padres (dos rutas) y se crea un gen inicial y otro final.
Luego, nos quedamos con aquellas ciudades que se encuentran desde
la posición gen inicial hasta la del gen final en unos de los padres.
Por ultimo, con el otro padre completamos las demas ciudades que faltan.
"""

def cruza(padre1, padre2):
    hijo = []
    hijoP1 = []
    hijoP2 = []

    genA = int(random.random() * len(padre1))
    genB = int(random.random() * len(padre1))

    genInicial = min(genA, genB)
    genFinal = max(genA, genB)

    for i in range(genInicial, genFinal):
        hijoP1.append(padre1[i])

    hijoP2 = [item for item in padre2 if item not in hijoP1]

    hijo = hijoP1 + hijoP2
    return hijo

"""
Una vez que determinamos quienes se aparean, obtenemos los hijos de las cruzas.
La cantidad de hijos que vamos a tener va a ser igual al tamaño del grupo de
apareamiento menos tamElite.

tamElite nos sirve a nosotros para excluir a las que no se van a cruzar.
"""

def cruzaPoblacion(grupoapareamiento, tamElite):
    hijos = []
    longitud = len(grupoapareamiento) - tamElite
    grupo = random.sample(grupoapareamiento, len(grupoapareamiento))

    for i in range(0, tamElite):
        hijos.append(grupoapareamiento[i])

    for i in range(0, longitud):
        hijo = cruza(grupo[i], grupo[len(grupoapareamiento) - i - 1])
        hijos.append(hijo)
    return hijos

def mutar(individuo, velocidadMutacion):
    for intercambio in range(len(individuo)):
        if (random.random() < velocidadMutacion):
            intercambiadoCon = int(random.random() * len(individuo))

            ciudad1 = individuo[intercambio]
            ciudad2 = individuo[intercambiadoCon]

            individuo[intercambio] = ciudad2
            individuo[intercambiadoCon] = ciudad1
    return individuo

"""
Por último, con la cruza ya realizada, realizamos la mutación con una
velocidad (o mejor dicho, probabilidad) de mutación. Cuando la velocidad
es 1, todos los individuos mutan.

Mutar significa, en este caso, cambiar la posicion de las ciudades (swap).
"""

def mutarPoblacion(poblacion, velocidadMutacion):
    mutardPop = []

    for ind in range(0, len(poblacion)):
        mutardInd = mutar(poblacion[ind], velocidadMutacion)
        mutardPop.append(mutardInd)
    return mutardPop

"""
Generamos la siguiente poblacion apartir de lo obtenido anteriormente.
"""

def proximaGeneracion(generacionActual, tamElite, velocidadMutacion):
    popRanqueada = rankingRutas(generacionActual)
    print("Pop Ranqueada: ", popRanqueada,"Tam Elite:", tamElite)
    seleccionResultados = seleccion(popRanqueada, tamElite)
    grupoapareamiento = grupoApareamiento(generacionActual, seleccionResultados)
    hijos = cruzaPoblacion(grupoapareamiento, tamElite)
    proximaGeneracion = mutarPoblacion(hijos, velocidadMutacion)
    return proximaGeneracion

def AlgoritmoGenetico(poblacion, tamPob, tamElite, velocidadMutacion, generaciones):
    pop = poblacionInicial(tamPob, poblacion)
    print("Distancia Inicial: " + str(1 / rankingRutas(pop)[0][1]))

    for i in range(0, generaciones):
        pop = proximaGeneracion(pop, tamElite, velocidadMutacion)

    print("Distancia Final: " + str(1 / rankingRutas(pop)[0][1]))
    IndiceMejorRuta = rankingRutas(pop)[0][0]
    mejorRuta = pop[IndiceMejorRuta]
    return mejorRuta

ciudadLista = []


for i in range(0,10):
    ciudadLista.append(Ciudad(x=int(random.random() * 200), y=int(random.random() * 200)))

# AlgoritmoGenetico(poblacion=ciudadLista, tamPob=100, tamElite=20, velocidadMutacion=0.01, generaciones=500)


def AlgoritmoGeneticoGraficar(poblacion, tamPob, tamElite, velocidadMutacion, generaciones):
    pop = poblacionInicial(tamPob, poblacion)
    print("Distancia Inicial: " + str(1 / rankingRutas(pop)[0][1]))
    progreso = []
    progreso.append(1 / rankingRutas(pop)[0][1])

    for i in range(0, generaciones):
        pop = proximaGeneracion(pop, tamElite, velocidadMutacion)
        progreso.append(1 / rankingRutas(pop)[0][1])
        print("Distancia: " + str(1 / rankingRutas(pop)[0][1]))

    print("Distancia Final: " + str(1 / rankingRutas(pop)[0][1]))

    plt.plot(progreso)
    plt.ylabel('Distancia')
    plt.xlabel('Generacion')
    plt.title(f'tamPob={tamPob}, tamElite={tamElite}, velocidadMutacion={velocidadMutacion}, generaciones={generaciones}')
    plt.show()
    print(*poblacion)

AlgoritmoGeneticoGraficar(poblacion=ciudadLista, tamPob=20, tamElite=10, velocidadMutacion=0, generaciones=50)
