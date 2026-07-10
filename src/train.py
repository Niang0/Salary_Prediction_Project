import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from src.logger import logger

def train_model(X, y):
    """
    Responsabilité UNIQUE : Entraîner le modèle, sauvegarder le fichier pkl 
    et retourner les résultats d'évaluation.
    """
    logger.info("Division des données en ensembles Train/Test...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    # Sécurité dossier
    os.makedirs("models", exist_ok=True)
    
    # Sauvegarde du modèle
    joblib.dump(model, "models/salary_model.pkl")
    logger.info("Fichier 'models/salary_model.pkl' sauvegardé avec succès.")
    
    return model, mae, r2