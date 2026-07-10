import pandas as pd
from sqlalchemy import text
from src.database import engine


def load_data():
    """
    Charge les données depuis la base de données PostgreSQL
    en effectuant une jointure pour récupérer le nom du département.
    """
    # On importe l'engine SQLAlchemy configuré dans votre database.py
    from src.database import engine 
    import pandas as pd

    # CORRECTION : On fait un JOIN pour récupérer le vrai nom textuel du département
    # et on le renomme en 'departement' pour l'harmoniser avec preprocess.py
    query = """
        SELECT 
            e.age,
            e.experience,
            d.name AS departement,
            e.salary AS salaire
        FROM employees e
        JOIN departments d ON e.department_id = d.id
    """
    
    df = pd.read_sql(query, engine)
    return df