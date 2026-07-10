from src.database import Base, engine
from src.models import Employee

Base.metadata.create_all(bind=engine)


print("✅ Base de données initialisée avec succès.")