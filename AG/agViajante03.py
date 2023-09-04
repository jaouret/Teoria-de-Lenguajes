import numpy as np, random, operator, pandas as pd, matplotlib.pyplot as plt

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

def crearRuta(ciudadList):
    ruta = random.sample(ciudadList, len(ciudadLista))
    return ruta

def poblacionInicial(tamPob, ciudadLista):
    poblacion = []

    for i in range(0, tamPob):
        poblacion.append(crearRuta(ciudadLista))
    return poblacion

def rankingRutas(poblacion):
    aptitudResultados = {}
    for i in range(0,len(poblacion)):
        aptitudResultados[i] = Aptitud(poblacion[i]).rutaAptitud()
    return sorted(aptitudResultados.items(), key = operator.itemgetter(1), reverse = True)

def seleccion(popRanqueada, tamElite):
    seleccionResultados = []
    df = pd.DataFrame(np.array(popRanqueada), columns=["Indice", "Aptitud"])
    df['cum_sum'] = df.Aptitud.cumsum()
    df['cum_perc'] = 100 * df.cum_sum / df.Aptitud.sum()

    for i in range(0, tamElite):
        seleccionResultados.append(popRanqueada[i][0])
    for i in range(0, len(popRanqueada) - tamElite):
        pick = 100 * random.random()
        for i in range(0, len(popRanqueada)):
            if pick <= df.iat[i, 3]:
                seleccionResultados.append(popRanqueada[i][0])
                break
    return seleccionResultados

def grupoApareamiento(poblacion, seleccionResultados):
    grupoapareamiento = []
    for i in range(0, len(seleccionResultados)):
        index = seleccionResultados[i]
        grupoapareamiento.append(poblacion[index])
    return grupoapareamiento

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

def mutarPoblacion(poblacion, velocidadMutacion):
    mutardPop = []

    for ind in range(0, len(poblacion)):
        mutardInd = mutar(poblacion[ind], velocidadMutacion)
        mutardPop.append(mutardInd)
    return mutardPop

def proximaGeneracion(generacionActual, tamElite, velocidadMutacion):
    popRanqueada = rankingRutas(generacionActual)
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


for i in range(0,35):
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
    plt.savefig('Gráfico.png')
    print(*poblacion)

AlgoritmoGeneticoGraficar(poblacion=ciudadLista, tamPob=100, tamElite=10, velocidadMutacion=0.01, generaciones=500)
