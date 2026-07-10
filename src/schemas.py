from pydantic import BaseModel


class EmployeeCreate(BaseModel):
      age:int

      experience:int

      department: str

      salary: float

      