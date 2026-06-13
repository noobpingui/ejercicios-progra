from pydantic import BaseModel, Field
from enum import Enum


#Enum/statuses definition
class TaskStatus(str, Enum):
    PorHacer = "Por Hacer"
    EnProgreso = "En Progreso"
    Completada = "Completada"

#Model definition
class Task(BaseModel):
    id: int = Field(gt=0) #validacion que int > 0
    title: str = Field(min_length=1) #validacion campo no puede ir vacio
    description: str = Field(min_length=1) #validacion campo no puede ir vacio
    status: TaskStatus #Solo acepta ENUM values y no puede ir vacio por lo mismo


# datos_validos = {

#     "id": 1,
#     "title": "test1",
#     "description": "Testing",
#     "status": "Completada"
# }

# new_task = Task(**datos_validos)

# print(new_task.id)
# print(new_task.title)
# print(new_task.description)
# print(new_task.status)
# print(new_task.status.value)
# print(new_task.model_dump())
# print(new_task.model_dump_json())