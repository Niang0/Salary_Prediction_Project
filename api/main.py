from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.logger import logger
from src.predict import load_model, predict_salary

from src.database import SessionLocal, Prediction, init_db, get_latest_predictions

from src.crud import get_all_employees
from src.crud import get_employee_by_id
from src.crud import create_employee
from src.schemas import EmployeeCreate
from src.crud import update_employee
from src.crud import delete_employee

app = FastAPI()

model = load_model()


class Employee(BaseModel):
    age: int
    experience: int
    finance: int
    it: int
    rh: int


@app.get("/")
def home():
    logger.info("Accueil de l'API.")
    return {
        "message": "Salary Prediction API"
    }


# --- CORRIGÉ : Maintenant on enregistre en BDD ---
@app.post("/predict")
def predict(employee: Employee):
    logger.info("Nouvelle prédiction demandée.")
    db = SessionLocal()

    try:
        # 1. Calcul de la prédiction via ton modèle scikit-learn
        prediction = predict_salary(
            model,
            [
                employee.age,
                employee.experience,
                employee.finance,
                employee.it,
                employee.rh,
            ],
        )

        # 2. Insertion dans la table 'predictions' de PostgreSQL
        new_prediction = Prediction(
            age=employee.age,
            experience=employee.experience,
            finance=employee.finance,
            it=employee.it,
            rh=employee.rh,
            predicted_salary=prediction  # On passe la valeur calculée
        )
        db.add(new_prediction)
        db.commit()  # On valide l'écriture en base de données
        logger.info(f"Salaire prédit : {prediction} et sauvegardé en BDD.")

        # 3. Retour de la réponse à Streamlit
        return {
            "predicted_salary": prediction
        }

    except Exception as e:
        db.rollback()
        logger.error(f"Erreur lors de l'enregistrement de la prédiction : {e}")
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        db.close()


@app.get("/employees")
def read_employees():
    db = SessionLocal()
    try:
        employees = get_all_employees(db)
        return employees
    finally: 
        db.close()


@app.get("/employees/{employee_id}")
def read_employee(employee_id: int):
    db = SessionLocal()
    try:
        employee = get_employee_by_id(db, employee_id)
        if employee is None:
            return {"message": "Employé introuvable" }
        return employee
    finally:
        db.close()


@app.post("/employees")
def add_employee(employee: EmployeeCreate):
    db = SessionLocal()
    try:
        new_employee = create_employee(
            db=db,
            age=employee.age,
            department=employee.department,
            salary=employee.salary,
        ) 
        return new_employee
    finally:
        db.close()


@app.put("/employees/{employee_id}")
def edit_employee(
    employee_id: int,
    employee: EmployeeCreate,
):
    # Correction subtile ici : il manquait les parenthèses () à SessionLocal
    db = SessionLocal()
    try:
        updated_employee = update_employee(
            db=db,
            employee_id=employee_id,
            age=employee.age,
            experience=employee.experience,
            departement=employee.department,
            salary=employee.salary,
        )
        if updated_employee is None:
            return {"message": "Employé introuvable"}
        return updated_employee
    finally:
        db.close()


@app.delete("/employe/{employee_id}")
def remove_employee(employee_id: int):
    # Correction subtile ici aussi : il manquait les parenthèses () à SessionLocal
    db = SessionLocal()
    try:
        employee = delete_employee(
            db,
            employee_id,
        )
        if employee is None:
            return {"message": "Employé introuvable"}
        return {"message": "Employé supprimé avec succès"}
    finally:
        db.close()


@app.get("/predictions")
def list_predictions(limit: int = 5):
    init_db() 
    db = SessionLocal()
    try:
        query = db.query(Prediction).order_by(Prediction.id.desc()).limit(limit).all()
        
        records = [
            {
                "ID": p.id,
                "Âge": p.age,
                "Expérience": p.experience,
                "Finance": p.finance,
                "IT": p.it,
                "RH": p.rh,
                "Salaire Prédit (FCFA)": p.predicted_salary,
                "Date": p.created_at.strftime("%Y-%m-%d %H:%M:%S") if p.created_at else None
            }
            for p in query
        ]
        return records
    except Exception as e:
        logger.error(f"🚨 ERREUR CRUCIAL BDD : {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()