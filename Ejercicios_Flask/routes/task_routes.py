#----------------#-----------------#
#SOLAMENTE LOS ENDPOINTS
#----------------#-----------------#
#To create blueprint
#To define routes/endpoints:
# GET /tasks
# POST /tasks
# PUT /tasks/<id>
# DELETE /tasks/<id>
# To receive REQUESTS and provide RESPONSES
#----------------#-----------------#

from flask import Blueprint, jsonify, request
from services.task_services import get_all_tasks, create_task, update_task, delete_task
from models.task import Task
from pydantic import ValidationError

#Blue Print registration
tasks_bp = Blueprint (
    'tasks_bp', __name__
)

#Routes

#GET
@tasks_bp.route('/')
def get_tasks():
    
    status_filter = request.args.get("status")
    body = get_all_tasks(status_filter)
        
    return (jsonify(body), 200)

#POST
@tasks_bp.route('/', methods=['POST'])
def post_tasks():

    try:
        body = request.get_json()
        new_task = Task(**body).model_dump()

        created_task = create_task(new_task)

        return (jsonify(created_task), 201)
    
    except ValidationError as error:
        return {"error": str(error)}, 400

    except ValueError as error:
        return {"error": str(error)}, 400

#PUT
@tasks_bp.route('/<int:task_id>', methods=['PUT'])
def put_tasks(task_id):
    
    try:
        body = request.get_json()
        new_task = Task(**body).model_dump()

        updated_task = update_task(task_id, new_task)

        return (jsonify(updated_task), 200)

    except ValidationError as error:
        return {"error": str(error)}, 400

    except ValueError as error:
        return {"error": str(error)}, 400

#DELETE
@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_tasks(task_id):
    
    try:
        delete_task(task_id)

        return {
            "message": f"Se elimino la tarea con el ID: {task_id}"
        }, 200  

    except ValueError as error:
        return {"error": str(error)}, 400