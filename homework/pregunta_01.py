"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""
import pandas as pd
import os


def limpiar_fecha(fecha):
    try:
        return pd.to_datetime(fecha, format="%Y/%m/%d")
    except ValueError:
        return pd.to_datetime(fecha, format="%d/%m/%Y")


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    df = pd.read_csv("files/input/solicitudes_de_credito.csv", sep=";", index_col=0)
    df = df.dropna()
      
    texto = ["sexo", "tipo_de_emprendimiento", "idea_negocio", "línea_credito"]
    for columna in texto:
        df[columna] = df[columna].str.lower()
        df[columna] = df[columna].str.replace("-", " ", regex=False)
        df[columna] = df[columna].str.replace("_", " ", regex=False)
        df[columna] = df[columna].str.replace(r"\s+", " ", regex=True)
        df[columna] = df[columna].str.translate(str.maketrans("", "", "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"))
        df[columna] = df[columna].str.strip()

    df["barrio"] = df["barrio"].str.lower().str.replace("-", " ", regex=False).str.replace("_", " ", regex=False)
    
    df["estrato"] = df["estrato"].astype(int)

    df["comuna_ciudadano"] = df["comuna_ciudadano"].astype(int)

    df["fecha_de_beneficio"] = df["fecha_de_beneficio"].apply(limpiar_fecha)

    df["monto_del_credito"] = (
        df["monto_del_credito"]
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.replace(".00", "", regex=False)
        .astype(float)
        .astype(int))

    df = df.drop_duplicates()
    
    os.makedirs("files/output", exist_ok=True)

    df.to_csv("files/output/solicitudes_de_credito.csv", sep=";", index=False)
