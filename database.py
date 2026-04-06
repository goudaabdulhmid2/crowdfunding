import json

DATA_FILE = "data.json"
current_user = None



def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            return {
                "users": data.get("users", []),
                "projects": data.get("projects", [])
            }
    except FileNotFoundError:
        return {"users": [], "projects": []}
    except json.JSONDecodeError:
        print("Error: Data file is corrupted. Starting with empty data.")
        return {"users": [], "projects": []}

def save_data(data):

    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def get_users():
    data = load_data()
    return data["users"]

def get_projects():
    data = load_data()
    return data["projects"]

def add_user(user):
    data = load_data()
    data["users"].append(user)
    save_data(data)

def add_project(project):
    data = load_data()
    data["projects"].append(project)
    save_data(data)
