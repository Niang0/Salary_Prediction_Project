from sqlalchemy.orm import Session

# import the Employee model from the models module 
# #for database operations
from src.models import Employee

# function to retrieve all employees from the database
def get_all_employees(db: Session):
    """
    Récupère tous les employés de la base de données.
    """
    return db.query(Employee).all()



def get_employee_by_id(db: Session, employee_id: int):
    """
    Récupère un employé par son ID de la base de données. 
    """
    return (
        db.query(Employee).filter(Employee.id == employee_id)
        .first()
        # cette méthode renvoie le premier employé 
        # correspondant à l'ID donné,
        #  ou None si aucun employé n'est trouvé.
    )

def create_employee(
        db: Session,
        age: int,
        experience:int,
        department: str,
        salary: float,
):
    
    employee = Employee(
        age=age,
        experience=experience,
        department=department,
        salary=salary,
    )
    db.add(employee)

    db.commit()

    db.refresh(employee)

    return employee


def update_employee(
        db: Session,
        employee_id:int,
        age:int,
        experience: int,
        department: str,
        salary: float,

):
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if employee is None:
        employee.age = age
        employee.experience = experience
        employee.department = department
        employee.salary = salary

        db.commit()

        db.refresh()

        return employee
    

def delete_employee(
        db: Session,
        employee_id: int,
):
    
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if employee is None:
        return None
    
    db.delete(employee)

    db.commit()

    return employee
