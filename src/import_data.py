import pandas as pd
from src.database import SessionLocal
from src.models import Employee, Department  # Assurez-vous d'importer Department

def import_csv_to_database():
    df = pd.read_csv("data/salaries.csv")
    session = SessionLocal()

    inserted = 0
    skipped = 0

    try:
        for _, row in df.iterrows():
            # 1. On cherche d'abord le département correspondant dans la base de données
            dept_name = row["departement"]
            db_department = session.query(Department).filter_by(name=dept_name).first()
            
            # Si le département n'existe pas encore en BDD, on le crée à la volée
            if db_department is None:
                db_department = Department(name=dept_name)
                session.add(db_department)
                session.flush()  # Permet de générer l'ID du département immédiatement

            # 2. On vérifie si l'employé existe déjà en filtrant par l'objet département trouvé
            existing_employee = session.query(Employee).filter_by(
                age=row["age"],
                experience=row["experience"],
                department=db_department,  # Ici on passe l'objet Department, ce que SQLAlchemy attend !
                salary=row["salaire"]
            ).first()
            
            # 3. Insertion si l'employé est nouveau
            if existing_employee is None:
                employee = Employee(
                    age=row["age"],
                    experience=row["experience"],
                    department=db_department,  # On lie l'objet ici aussi
                    salary=row["salaire"]
                )
                session.add(employee)
                inserted += 1
            else:
                skipped += 1

        session.commit()
        print("✅ Les données ont été traitées avec succès.")
        print(f"-> {inserted} employés ajoutés.")
        print(f"-> {skipped} employés ignorés (déjà existants).")

    except Exception as e:
        session.rollback()
        print("Erreur lors de l'import :", e)

    finally:
        session.close()

if __name__ == "__main__":
    import_csv_to_database()