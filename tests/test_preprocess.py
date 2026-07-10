import pandas as pd
import pytest
from src.preprocess import encode_department, split_features_target

def test_encode_department():
    """
    Vérifie que l'encodage One-Hot crée bien les bonnes colonnes
    et supprime la colonne d'origine.
    """
    # 1. On crée un mini DataFrame de test en entrée
    data = {
        "age": [25, 30],
        "experience": [2, 5],
        "departement": ["IT", "Finance"]
    }
    df = pd.DataFrame(data)
    
    # 2. On applique la fonction
    df_encoded = encode_department(df)
    
    # 3. Les assertions (vérifications)
    # On vérifie que la colonne d'origine 'departement' a bien été supprimée
    assert "departement" not in df_encoded.columns
    
    # On vérifie que les nouvelles colonnes d'encodage existent
    assert "IT" in df_encoded.columns
    assert "Finance" in df_encoded.columns
    assert "RH" in df_encoded.columns
    
    # On vérifie la valeur de l'encodage pour la première ligne (IT)
    assert df_encoded.loc[0, "IT"] == 1
    assert df_encoded.loc[0, "Finance"] == 0

def test_split_features_target():
    """
    Vérifie que la séparation entre les features (X) et la cible (y)
    se fait correctement.
    """
    # 1. On crée un DataFrame simulé après encodage
    data = {
        "age": [25, 30],
        "experience": [2, 5],
        "Finance": [0, 1],
        "IT": [1, 0],
        "RH": [0, 0],
        "salaire": [350000, 500000]
    }
    df = pd.DataFrame(data)
    
    # 2. On applique la fonction
    X, y = split_features_target(df)
    
    # 3. Les assertions
    # X ne doit pas contenir la colonne cible 'salaire'
    assert "salaire" not in X.columns
    # X doit contenir toutes les autres colonnes (5 features)
    assert X.shape[1] == 5
    # y doit être une Series (ou un tableau) contenant uniquement les salaires
    assert len(y) == 2
    assert y.iloc[0] == 350000