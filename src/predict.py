import joblib
from src.logger import logger
import pandas as pd

def load_model():
    """
    Charge le modèle sauvegardé.
    """

    try:

        logger.info("Chargement du modèle...")

        model = joblib.load("models/salary_model.pkl")

        logger.info("Modèle chargé avec succès.")

        return model

    except Exception as e:

        logger.error(f"Erreur lors du chargement du modèle : {e}")

        raise


def predict_salary(model, features):
    """
    Retourne une prédiction.
    """
    # Définir précisément l'ordre et le nom des colonnes utilisées à l'entraînement
    feature_names = ["age", "experience", "Finance", "IT", "RH"]
    
    # Si 'features' est passé comme une liste plate (1D), on l'enrobe dans une liste de lignes
    if isinstance(features, list) and not isinstance(features[0], list):
        data = [features]
    else:
        data = features

    # Création du DataFrame avec les noms de features pour ravir Scikit-Learn
    df_features = pd.DataFrame(data, columns=feature_names)

    # Prédiction sur le DataFrame clean
    prediction = model.predict(df_features)

    return float(prediction[0])