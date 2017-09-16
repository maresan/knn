from random import shuffle
from math import sqrt
import operator
import csv

def cargarDatos(archivo):
    entrenamiento = []
    pruebas = []
    with open(archivo, 'rb') as csvfile:
        lineas = csv.reader(csvfile)
        dataset = list(lineas)
        shuffle(dataset)
        for i in range(len(dataset)):
            for j in range(len(dataset[0])-1):
                dataset[i][j] = float(dataset[i][j])
            if i < len(dataset)*0.9:
                entrenamiento.append(dataset[i])
            else:
                pruebas.append(dataset[i])
    return entrenamiento, pruebas

def calcularDistancia(pruebas, entrenamiento):
    distancia = 0
    for i in range(len(pruebas)-1):
        distancia = (distancia + pruebas[i] - entrenamiento[i])**2
    return sqrt(distancia)
 
def obtenerDistancias(entrenamiento, pruebas):
    distancias = []
    for i in range(len(entrenamiento)):
        distancia = calcularDistancia(pruebas, entrenamiento[i])
        distancias.append((entrenamiento[i], distancia))
    distancias.sort(key=operator.itemgetter(1))
    return distancias

def obtenerVecinos(distancias, k):
    vecinos = []
    for i in range(k):
        vecinos.append(distancias[i][0])
    return vecinos

def generarPrediccion(vecinos):
    aux = {}
    for i in range(len(vecinos)):
        prediccion = vecinos[i][-1]
        if prediccion in aux:
            aux[prediccion] = aux[prediccion] + 1
        else:
            aux[prediccion] = 1
    sorteo = sorted(aux.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sorteo[0][0]
 
def calcularPorcentaje(pruebas, predicciones):
    correcta = 0
    for i in range(len(pruebas)):
        if pruebas[i][-1] == predicciones[i]:
            correcta += 1
    aux = float(len(pruebas))
    return (correcta/aux) * 100.0

#-----------------------------------------------------------------------------------------------------------------------
#----------------------------------------- Menu Principal --------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------

predicciones=[]
k = 1
entrenamiento, pruebas  = cargarDatos("iris_dataset.csv")
for i in range(len(pruebas)):
    distancias = obtenerDistancias(entrenamiento, pruebas[i])
    prediccion = generarPrediccion(obtenerVecinos(distancias, k))
    predicciones.append(prediccion)
    print("Prediccion: {} actual: {}"). format(str(prediccion), str(pruebas[i][-1]) )
print "Porcentaje de certeza: {} %".format(str(calcularPorcentaje(pruebas, predicciones)))
