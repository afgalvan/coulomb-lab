"""
Funciones útiles para el computo y registro en el laboratorio de la
ley de Coulomb
"""

from typing import List
from pandas import DataFrame
import matplotlib.pyplot as plt

RegistroFuerza = tuple[float, float]
RegistroCarga = tuple[RegistroFuerza, float]


def crear_dataframe() -> DataFrame:
    """
    Crear dataframe base con las columnas requeridas en el laboratorio 
    """
    return DataFrame(
        index=range(1, 21),
        columns=["F (N)", "r (pm)", "r (mts)", "1/r²"]
    ).rename_axis("N°", axis=1)


def pm_a_mts(pm: float) -> float:
    """
    Convertir un valor dado en pm a mts
    """
    return pm * (10 ** -12)


def inverso_cuadrado(distancia: float) -> float:
    """
    Realiza el cálculo del inverso al cuadrado de una distancia
    """
    return 1 / (distancia ** 2)


def nuevo_registro(fuerza: RegistroFuerza, distancia: float) -> List[float]:
    """
    Crea una nueva fila para ser añadido al dataframe
    """
    distancia_mts: float = pm_a_mts(distancia)
    return [fuerza[0] * (10 ** fuerza[1]), distancia, distancia_mts, inverso_cuadrado(distancia_mts)]


def registrar_cargas(dataframe: DataFrame, *registros: RegistroCarga) -> None:
    """
    Registrar en el dataframe recibido n cantidad de registros de cargas
    """
    for i, registro in enumerate(registros):
        dataframe.loc[i + 1] = nuevo_registro(registro[0], registro[1])


def registrar(dataframe: DataFrame, *registros: RegistroFuerza, inicio=0, paso=0) -> None:
    """
    Registrar en el dataframe recibido n cantidad de registros de fuerza
    y automatizar las distancias con los parametros recibidos en inicio y paso
    """
    for i, registro in enumerate(registros):
        dataframe.loc[i + 1] = nuevo_registro(registro, inicio)
        inicio += paso

def graficar(titulo: str, dataframe: DataFrame, x="r (pm)", color="#3EA6FF") -> None:
    plt.style.use("seaborn-whitegrid")
    plt.rcParams.update({"figure.figsize": (7,5), "figure.dpi": 100})
    plt.plot(dataframe[x].tolist(), dataframe["F (N)"].tolist(),
        color=color, marker=".", markerfacecolor=color,
    )
    plt.title(titulo)
    plt.ylabel("F (N)")
    plt.xlabel(x)
    if (x == "r (pm)"):
        plt.xlim(0, 110)
    plt.show()


def error_porcentual(aceptado: float, experimental: float) -> float:
    return ((aceptado - experimental) / aceptado) * 100
