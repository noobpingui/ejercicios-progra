#----------------#-----------------#
#To start the app and register routes
#----------------#-----------------#
from flask import Flask
from routes import task_routes


app = Flask(__name__)

#Routes registration
app.register_blueprint(task_routes.tasks_bp, url_prefix='/tasks')

#To run the app
if __name__ == "__main__":
    app.run(
        host="localhost",
        port=5000, 
        debug=True
    )







