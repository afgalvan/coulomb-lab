"""
Funciones útiles para el computo y registro en el laboratorio de la
ley de Coulomb
"""

from typing import List, Tuple
from pandas import DataFrame

RegistroFuerza = tuple[float, float]
RegistroCarga = tuple[RegistroFuerza, float]

def crear_dataframe() -> DataFrame:
    """
    Crear dataframe base con las columnas requeridas en el laboratorio 
    """
    return DataFrame(
        index=range(1, 21),
        columns=["F (N)", "r (pm)", "1/r²"]
    ).rename_axis("N°", axis=1)


def nuevo_registro(fuerza: RegistroFuerza, distancia: float) -> List[float]:
    """
    Crea una nueva fila para ser añadido al dataframe
    """
    return [fuerza[0] * (10 ** fuerza[1]), distancia, 1 / (distancia**2)]


def registrar(dataframe: DataFrame, *registros: RegistroFuerza, inicio=0, paso=0) -> None:
    """
    Registrar en el dataframe recibido n cantidad de registros de fuerza
    y automatizar las distancias con los parametros recibidos en inicio y paso
    """
    for i, registro in enumerate(registros):
        dataframe.loc[i + 1] = nuevo_registro(registro, inicio)
        inicio += paso


def registrar(dataframe: DataFrame, *registros: RegistroCarga) -> None:
    """
    Registrar en el dataframe recibido n cantidad de registros de cargas
    """
    for i, registro in enumerate(registros):
        dataframe.loc[i + 1] = nuevo_registro(registro[0], registro[1])


def pm_a_mts(pm: float) -> float:
    """
    Convertir un valor dado en pm a mts
    """
    return pm * (10**-12)
