"""
Funciones útiles para el computo y registro en el laboratorio de la
ley de Coulomb
"""

from typing import List
from pandas import DataFrame
from numpy import polyfit
from math import pi
import matplotlib.pyplot as plt


class DatosExperimentacion():
    def __init__(self, fuerza: List[float], inverso_r: List[float], q1: float, q2: float) -> None:
        self.q1 = q1
        self.q2 = q2
        self.fuerza = fuerza
        self.inverso_r = inverso_r


RegistroCarga = tuple[float, float]


def crear_dataframe(max_limit=20) -> DataFrame:
    """
    Crear dataframe base con las columnas requeridas en el laboratorio 
    """
    return DataFrame(
        index=range(1, max_limit + 1),
        columns=["F (N)", "r (pm)", "r (mts)", "1/r²"]
    ).rename_axis("N°", axis=1)


def E(base: float, exponente: float) -> float:
    return base * (10 ** exponente)


def pm_a_mts(pm: float) -> float:
    """
    Convertir un valor dado en pm a mts
    """
    return E(pm, -12)


def inverso_cuadrado(distancia: float) -> float:
    """
    Realiza el cálculo del inverso al cuadrado de una distancia
    """
    return 1 / (distancia ** 2)


def nuevo_registro(fuerza: float, distancia: float) -> List[float]:
    """
    Crea una nueva fila para ser añadido al dataframe
    """
    distancia_mts: float = pm_a_mts(distancia)
    return [fuerza, distancia, distancia_mts, inverso_cuadrado(distancia_mts)]


def registrar_cargas(dataframe: DataFrame, *registros: RegistroCarga) -> None:
    """
    Registrar en el dataframe recibido n cantidad de registros de cargas
    """
    for i, registro in enumerate(registros):
        dataframe.loc[i + 1] = nuevo_registro(registro[0], registro[1])


def registrar(dataframe: DataFrame, *registros: float, inicio=0, paso=0) -> None:
    """
    Registrar en el dataframe recibido n cantidad de registros de fuerza
    y automatizar las distancias con los parametros recibidos en inicio y paso
    """
    distancia = inicio
    for i, registro in enumerate(registros):
        dataframe.loc[i + 1] = nuevo_registro(registro, distancia)
        distancia += paso


def graficar(titulo: str, dataframe: DataFrame, x="r (pm)", color="#3EA6FF") -> None:
    """
    Grafica de fuerza en newtons vs distancia en una base dada
    """
    plt.style.use("seaborn-whitegrid")
    plt.plot(dataframe[x].tolist(), dataframe["F (N)"].tolist(),
             color=color, marker=".", markerfacecolor=color,
             )
    plt.rcParams.update({"figure.figsize": (7, 5), "figure.dpi": 100})
    plt.title(titulo)
    plt.ylabel("F (N)")
    plt.xlabel(x)
    if (x == "r (pm)"):
        plt.xlim(0, 45)
    plt.show()


def error_porcentual(aceptado: float, experimental: float) -> str:
    """
    Calcular error porcentual de un resultado experimental obtenido con
    respecto al aceptado
    """
    return "{:.2f}%".format(((aceptado - experimental) / aceptado) * 100)


def resultado_experimentacion(*resultados: DatosExperimentacion) -> DataFrame:
    K_ACEPTADA = constante_aceptada()
    experimentales = [calcular_resultado(x) for x in resultados]
    errores = [error_porcentual(K_ACEPTADA, k) for k in experimentales]

    return DataFrame({
        "Valor": [f"ke{i+1}" for i in range(len(resultados))],
        "Experimental": experimentales,
        "Teórico": [K_ACEPTADA for _ in range(len(resultados))],
        "Error Porcentual": errores
    })


def calcular_resultado(resultado: DatosExperimentacion) -> float:
    p = polyfit(resultado.inverso_r, resultado.fuerza, 1)
    m = p[0]

    return constante_experimental(m, resultado.q1, resultado.q2)


def constante_experimental(m: float, q1: float, q2: float) -> float:
    """
    Calcular constante de coulomb de manera experimental
    """
    e = 1.6022e-19
    return m / abs((q1 * e) * (q2 * e))


def constante_aceptada() -> float:
    """
    Calcular la constante de Coulomb mediante la formula ya establecida
    """
    E0 = 8.8542e-12
    return 1 / (4 * pi * E0)
