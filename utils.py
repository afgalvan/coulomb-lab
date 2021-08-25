from pandas import DataFrame

def crear_dataframe() -> DataFrame:
    return DataFrame(
        index=range(20),
        columns=["F (N)", "r (pm)", "1/r²"]
    ).rename_axis("N°", axis=1)