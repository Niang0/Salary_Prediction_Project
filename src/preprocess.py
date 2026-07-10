import pandas as pd
from src.data_loader import load_data


def encode_department(df):
    """
    Transforme la colonne 'departement' en variables numériques (One-Hot Encoding).
    """
    # Correction ici : on utilise "departement" avec un "e" (comme configuré dans le SQL alias)
    # Et on fait attention à la casse des valeurs stockées ("Finance", "IT", "RH")
    df["Finance"] = (df["departement"] == "Finance").astype(int)
    df["IT"] = (df["departement"] == "IT").astype(int)
    df["RH"] = (df["departement"] == "RH").astype(int)

    # On supprime la colonne d'origine en spécifiant le bon nom français
    df.drop(columns=["departement"], inplace=True)

    return df


def split_features_target(df):
    """
    Sépare les features (X)
    de la target (y).
    """
    X = df.drop("salaire", axis=1)
    y = df["salaire"]
    return X, y

