#----------------#-----------------#
#TODA LA LOGICA DE NEGOCIO
#----------------#-----------------#
# Business Logic
# Read-Write JSON
# Find-Create-Update-Delete TASKS
# Validations 
#----------------#-----------------#

import json
from exceptions.task_exceptions import TaskNotFoundError, DuplicateTaskIdError

#Task functions

#To get/read the JSON file with all the tasks
def read_tasks():
    with open('data/tasks.json', 'r') as json_file:
        task_data = json.load(json_file)
    
    return task_data

#To save/write a new task list in the JSON file.
def save_tasks(task_data):
    with open('data/tasks.json', 'w') as json_file:
        json.dump(task_data,json_file, indent=4)

#To create a new task
def create_task(new_task):
    task_data = read_tasks()
    
    for task in task_data:
        if task["id"] == new_task["id"]:
            raise DuplicateTaskIdError("Ids duplicados, abortando operacion")
        
    task_data.append(new_task)
    
    save_tasks(task_data)

    return new_task

#To list all the tasks and filter according to the query parameters
def get_all_tasks(status_filter=None):
    task_data = read_tasks()

    if status_filter:
        task_data = list(
            filter(lambda current_task: current_task["status"] == status_filter, task_data)
        )    
        
    return task_data

#To update a task based on the url parameter <id>
def update_task(task_id, new_task):
    task_data = read_tasks()

    for task in task_data:
        if task["id"] == task_id:
            task.update(new_task)
            save_tasks(task_data)

            return new_task    
        
    raise TaskNotFoundError("No existe un task con ese id")

#To delete a task based on the url parameter <id>
def delete_task(task_id):
    task_data = read_tasks()

    for index, task in enumerate(task_data):
        if task["id"] == task_id:
            task_data.pop(index)
            save_tasks(task_data)  
            
            return None
        
    raise TaskNotFoundError("No existe un task con ese id")