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
        f"{project_name}/.gitignore": GITIGNORE,
        f"{project_name}/README.md": README_MD,
        f"{project_name}/requirements.txt": REQUIREMENTS_TXT,
        f"{project_name}/run.py": RUN_PY,
        f"{project_name}/app/__init__.py": INIT_PY,
        f"{project_name}/app/settings.py": SETTINGS_PY.format(app_name=project_name),
        f"{project_name}/app/routes/__init__.py": ROUTES_INIT_PY,
        f"{project_name}/app/routes/users_routes.py": USERS_ROUTES_PY,
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

def is_git_installed():
    try:
        subprocess.run(["git", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False

def initialize_git_repo(project_name):
    if not is_git_installed():
        print("Error: Git is not installed. Please install Git and try again.")
        return
    os.chdir(project_name)
    try:
      subprocess.run(["git", "init"], check=True)
      subprocess.run(["git", "add", "."], check=True)
      subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during Git operations: {e}")
        return
    finally:
        os.chdir("..")
        print("\n[+] Git repository initialized and initial commit created.")

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
API_KEY=your_sample_api_key
'''

FLASKENV = '''\
FLASK_APP=app
FLASK_RUN_HOST=0.0.0.0
FLASK_DEBUG=True
FLASK_RUN_PORT=5000
'''

GITIGNORE = '''\
# Python
__pycache__/
.env
.venv/

# Flask
instance/
*.pyc

# General
.DS_Store
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
import os
from dotenv import load_dotenv

load_dotenv('.env')

API_KEY = os.getenv('API_KEY')
APP_VERSION = '1.0'
APP_NAME = '{app_name}'
'''

ROUTES_INIT_PY = """\
from flask_swagger_ui import get_swaggerui_blueprint
from app.routes.users_routes import users_blueprint

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
    app.register_blueprint(users_blueprint, url_prefix="/api/users")
"""

USERS_ROUTES_PY = """\
from flask import Blueprint, jsonify, current_app, request

users_blueprint = Blueprint("users", __name__)

@users_blueprint.get("/")
def get_users():
    '''
        get users list
        ---
        tags:
          - users
            
        responses:
          200:
            description: User List
    '''
    db = current_app.extensions["db"]
    data = db.users.find_one({},{'_id':0})
    return jsonify(data)

@users_blueprint.get("/<user_id>")
def get_user(user_id):
    '''
        get user with mongodb's ObjectId
        ---
        tags:
          - users
            
        responses:
          201:
            description: User Found
          404:
            description: User Not Found
    '''
    db = current_app.extensions["db"]
    ObjectId = current_app.extensions['ObjectId']
    data = db.users.find_one({'_id': ObjectId(user_id)},{'_id':0})
    return (jsonify(data), 201) if data else (jsonify({'message':'User Not Found'}), 404)
"""


if __name__ == "__main__":
    project_name = input("Enter the project name: ")
    create_project_structure(project_name)
    setup_virtualenv(project_name)
    get_swagger_sample_doc_json(project_name)
    initialize_git_repo(project_name)
    print_success_message(project_name)
