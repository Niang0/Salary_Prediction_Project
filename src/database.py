from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
import pandas as pd
from src.config import (
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_NAME,
    DATABASE_USER,
    DATABASE_PASSWORD,
)

DATABASE_URL = (
    f"postgresql+psycopg://{DATABASE_USER}:{DATABASE_PASSWORD}"
    f"@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()

# Modèle pour la table des prédictions
class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer, nullable=False)
    experience = Column(Integer, nullable=False)
    finance = Column(Integer, nullable=False)
    it = Column(Integer, nullable=False)
    rh = Column(Integer, nullable=False)
    predicted_salary = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Fonction pour créer la table automatiquement
def init_db():
    Base.metadata.create_all(bind=engine)

# ... (garde tout ton code actuel et ajoute ça tout en bas)

def get_latest_predictions(limit=10):
    """Récupère les X dernières prédictions sous forme de DataFrame Pandas"""
    db = SessionLocal()
    try:
        # Requête SQLAlchemy pour trier par ID décroissant
        query = db.query(Prediction).order_by(Prediction.id.desc()).limit(limit)
        
        # Transformation en liste de dictionnaires pour Pandas
        data = [
            {
                "ID": p.id,
                "Âge": p.age,
                "Expérience": p.experience,
                "Finance": p.finance,
                "IT": p.it,
                "RH": p.rh,
                "Salaire Prédit (FCFA)": p.predicted_salary,
                "Date": p.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }
            for p in query
        ]
        return pd.DataFrame(data)
    finally:
        db.close()