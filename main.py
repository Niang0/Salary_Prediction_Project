from src.data_loader import load_data  # Ajuste l'import selon ton projet réel
from src.preprocess import encode_department, split_features_target
from src.train import train_model
from src.config import DATABASE_HOST
from src.logger import logger

def main():
    """
    Responsabilité UNIQUE : Orchestrer le pipeline complet du projet.
    """
    logger.info("Démarrage du pipeline global d'entraînement.")
    logger.info(f"Contexte BDD : {DATABASE_HOST}")

    # 1. Charger les données
    logger.info("Chargement des données depuis data/salaries.csv...")
    df = load_data("data/salaries.csv")

    # 2. Encoder les variables catégorielles
    logger.info("Encodage des variables catégorielles...")
    df = encode_department(df)

    # 3. Séparer les features et la cible
    X, y = split_features_target(df)

    # 4. Entraîner le modèle (Appel du module pur src.train)
    logger.info("Lancement de l'entraînement...")
    model, mae, r2 = train_model(X, y)

    # 5. Affichage des performances
    print("=" * 40)
    print("RÉSULTATS DU MODÈLE LOGUÉS AVEC SUCCÈS")
    print("=" * 40)
    print(f"MAE : {mae:.2f} FCFA")
    print(f"R²  : {r2:.2f}")
    
    logger.info(f"Pipeline terminé. Métriques finales -> MAE: {mae:.2f} | R²: {r2:.2f}")

if __name__ == "__main__":
    main()