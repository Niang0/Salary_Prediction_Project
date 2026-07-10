import pandas as pd
from src.data_loader import load_data

def test_load_data_returns_dataframe():
    """
    Vérifie que load_data retourne un DataFrame Pandas non vide
    et contient les colonnes attendues.
    """
    # 1. On appelle la fonction de chargement
    df = load_data()
    
    # 2. Les assertions
    assert isinstance(df, pd.DataFrame), "Le résultat doit être un DataFrame Pandas"
    assert not df.empty, "Le DataFrame ne doit pas être vide"
    
    # Vérification de la présence des colonnes minimales requises
    expected_columns = ["age", "experience", "departement", "salaire"]
    for col in expected_columns:
        assert col in df.columns, f"La colonne manquante dans la base de données : {col}"