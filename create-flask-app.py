import os
import subprocess
import json

def create_project_structure(project_name):
    folders = [
        f"{project_name}/app",
        f"{project_name}/app/docs",
        f"{project_name}/app/routes",
        f"{project_name}/app/models",
        f"{project_name}/app/schemas",
        f"{project_name}/app/utils",
        f"{project_name}/migrations",
        f"{project_name}/tests"
    ]
    print('\n[+] creating directories')
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

    files = {
        f"{project_name}/.env": ENV,
        f"{project_name}/.flaskenv": FLASKENV,
        f"{project_name}/README.md": README_MD,
        f"{project_name}/requirements.txt": REQUIREMENTS_TXT,
        f"{project_name}/run.py": RUN_PY,
        f"{project_name}/app/__init__.py": INIT_PY,
        f"{project_name}/app/settings.py": SETTINGS_PY.format(app_name=project_name),
        f"{project_name}/app/routes/__init__.py": ROUTES_INIT_PY,
        f"{project_name}/app/routes/user_routes.py": USER_ROUTES_PY,
        f"{project_name}/app/models/__init__.py": "",
        f"{project_name}/app/schemas/__init__.py": "",
    }
    
    print('\n[+] creating files')
    for file_path, content in files.items():
        with open(file_path, "w") as file:
            file.write(content)

def setup_virtualenv(project_name):
    print('\n[+] creating virtual environment')
    venv_path = os.path.join(project_name, ".venv")
    subprocess.run(["python", "-m", "venv", venv_path])

    print('\n[+] installing requirements')
    if os.name=='nt':
        subprocess.run([os.path.join(venv_path, "Scripts", "pip"), "install", "-r", f"{project_name}/requirements.txt"])
    else:
        subprocess.run([os.path.join(venv_path, "bin", "pip"), "install", "-r", f"{project_name}/requirements.txt"])
    
def get_swagger_sample_doc_json(project_name):
    print('\n[+] Downloading swagger sample API Doc json')
    os.system(f'curl https://petstore.swagger.io/v2/swagger.yaml > {project_name}/app/docs/swagger_sample_api_doc.yaml')

def print_success_message(project_name):
    print()
    print(format(' SUCCESS ','=^30'))
    print(f"Project {project_name} created successfully!")
    print(f"Navigate to the {project_name} directory, activate the virtual environment, and run the app:")
    print(f"  1. cd {project_name}")
    print(f"  2. source .venv/bin/activate #if linux or mac")
    print(f"  3. .venv\\Scripts\\activate.bat #if windows")
    print(f"  4. flask run")


# content for project files
ENV = '''\
'''

FLASKENV = '''\
FLASK_APP=app
FLASK_RUN_HOST=0.0.0.0
FLASK_DEBUG=True
FLASK_RUN_PORT=5000
'''

README_MD = '''\
## create-flask-app
this app provides an easy setup for Flask REST project.
Swagger API docmentaion has been used in this project by default.
to see all the endpoints use url http://localhost:5000/swagger
'''

REQUIREMENTS_TXT = '''\
Flask==3.1.0
Flask_Cors==5.0.0
Flask_Swagger==0.2.14
Flask_Swagger_UI==4.11.1
Python-Dotenv==1.0.1
'''

RUN_PY = """\
from app import app

if __name__ == "__main__":
    app.run(debug=True)
"""

INIT_PY = """\
from flask import Flask, jsonify
from flask_cors import CORS
from flask_swagger import swagger

from app.routes import register_routes

app = Flask(__name__)
app.config.from_pyfile('settings.py')
CORS(app=app)
register_routes(app)

@app.route('/api_doc_json')
def get_api_doc_json():
    swag = swagger(app)
    swag['info']['version'] = app.config['APP_VERSION']
    swag['info']['title'] = app.config['APP_NAME']
    return jsonify(swag)
"""

SETTINGS_PY = '''\
APP_VERSION = '1.0'
APP_NAME = '{app_name}'
'''

ROUTES_INIT_PY = """\
from flask_swagger_ui import get_swaggerui_blueprint
from app.routes.user_routes import user_blueprint

# Swagger UI route
SWAGGER_URL = '/swagger'
API_URL = '/api_doc_json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Swagger'
    }
)

def register_routes(app):
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    app.register_blueprint(user_blueprint, url_prefix="/api/user")
"""

USER_ROUTES_PY = """\
from flask import Blueprint, jsonify

user_blueprint = Blueprint("user", __name__)

@user_blueprint.route("/", methods=["GET"])
def get_user():
    '''
        get all users
        ---
        tags:
          - users
        definitions:
          - schema:
              id: Group
              properties:
                name:
                 type: string
                 description: the group's name
        parameters:
          - in: body
            name: body
            schema:
              id: User
              required:
                - email
                - name
              properties:
                email:
                  type: string
                  description: email for user
                name:
                  type: string
                  description: name for user
                address:
                  description: address for user
                  schema:
                    id: Address
                    properties:
                      street:
                        type: string
                      state:
                        type: string
                      country:
                        type: string
                      postalcode:
                        type: string
                groups:
                  type: array
                  description: list of groups
                  items:
                    $ref: "#/definitions/Group"
        responses:
          201:
            description: User created
    '''
    return jsonify({"message": "Hello, Flask RESTful API!"})
"""


if __name__ == "__main__":
    project_name = input("Enter the project name: ")
    create_project_structure(project_name)
    setup_virtualenv(project_name)
    get_swagger_sample_doc_json(project_name)
    print_success_message(project_name)
