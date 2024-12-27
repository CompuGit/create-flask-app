import os
import subprocess

def create_project_structure(project_name):
    folders = [
        f"{project_name}/app",
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
        f"{project_name}/run.py": RUN_PY_CONTENT,
        f"{project_name}/app/__init__.py": INIT_PY_CONTENT,
        f"{project_name}/app/routes/__init__.py": ROUTES_INIT_CONTENT,
        f"{project_name}/app/routes/sample_routes.py": SAMPLE_ROUTE_CONTENT,
        f"{project_name}/app/models/__init__.py": "",
        f"{project_name}/app/schemas/__init__.py": "",
        f"{project_name}/requirements.txt": "Flask==3.1.0\n",
        f"{project_name}/README.md": f"# {project_name}\n\nA Flask RESTful API project.",
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
    
def print_success_message(project_name):
    print()
    print(format(' SUCCESS ','=^30'))
    print(f"Project {project_name} created successfully!")
    print(f"Navigate to the {project_name} directory, activate the virtual environment, and run the app:")
    print(f"  1. cd {project_name}")
    print(f"  2. source .venv/bin/activate #if linux or mac")
    print(f"  3. .venv\\Scripts\\activate.bat #if windows")
    print(f"  4. python run.py")

# Sample content for project files
RUN_PY_CONTENT = """\
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
"""

INIT_PY_CONTENT = """\
from flask import Flask
from app.routes import register_routes

def create_app():
    app = Flask(__name__)
    register_routes(app)
    return app
"""

ROUTES_INIT_CONTENT = """\
from app.routes.sample_routes import sample_blueprint

def register_routes(app):
    app.register_blueprint(sample_blueprint, url_prefix="/api/sample")
"""

SAMPLE_ROUTE_CONTENT = """\
from flask import Blueprint, jsonify

sample_blueprint = Blueprint("sample", __name__)

@sample_blueprint.route("/", methods=["GET"])
def get_sample():
    return jsonify({"message": "Hello, Flask RESTful API!"})
"""

if __name__ == "__main__":
    project_name = input("Enter the project name: ")
    create_project_structure(project_name)
    setup_virtualenv(project_name)
    print_success_message(project_name)
