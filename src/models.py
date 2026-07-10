from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship 

from src.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)

    age = Column(Integer, nullable=False)

    experience = Column(Integer, nullable=False)

    salary = Column(Float, nullable=False)

    department_id = Column(Integer,
                        ForeignKey("departments.id"),
                         nullable=False)

    department = relationship(
        "Department",
        back_populates="employees"
    )
    

class Department(Base):

    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, unique=True, nullable=False)

    employees = relationship(
        "Employee",
        back_populates="department"
    )