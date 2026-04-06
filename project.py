import database
from utils import (
    validate_required,
    validate_positive_number,
    validate_date_format,
    validate_start_end_dates,
    validate_choice,
)
from auth import logout


def print_project(project, index=None, show_owner=True):
    if index is not None:
        print(f"\nProject #{index}")

    print(f"Title: {project['title']}")
    print(f"Details: {project['details']}")
    print(f"Target: {project['total_target']}")
    print(f"Start Date: {project['start_date']}")
    print(f"End Date: {project['end_date']}")

    if show_owner:
        print(f"Owner: {project['owner_email']}")

    print("-" * 30)


def get_current_user_projects(projects):
    owner_email = database.current_user["email"]
    return [project for project in projects if project["owner_email"] == owner_email]


def show_project_menu():
    while True:
        print("\n=== Project Menu ===")
        print("1. Create Project")
        print("2. View My Projects")
        print("3. View All Projects")
        print("4. Edit Own Projects")
        print("5. Delete Own Projects")
        print("6. Search Projects By Date")
        print("7. Logout and Return to Main Menu")

        choice = input("Enter your choice: ")

        match choice:
            case "1":
                create_project()
            case "2":
                view_my_projects()
            case "3":
                view_all_projects()
            case "4":
                edit_project()
            case "5":
                delete_project()
            case "6":
                search_projects_by_date()
            case "7":
                print("Logging out and returning to the main menu.")
                logout()
                break
            case _:
                print("Invalid choice. Please try again.")

def create_project():
    new_project = {}
    try:
        if database.current_user is None:
            print("You must be logged in to create a project.")
            return

        title = input("Enter project title: ")
        title = validate_required(title, "Project Title")
        new_project["title"] = title

        details = input("Enter project details: ")
        details = validate_required(details, "Project Details")
        new_project["details"] = details

        total_target = input("Enter total target amount: ")
        total_target = validate_required(total_target, "Total Target")
        total_target = validate_positive_number(total_target, "Total Target")
        new_project["total_target"] = total_target

        start_date = input("Enter project start date (YYYY-MM-DD): ")
        start_date = validate_required(start_date, "Start Date")
        start_date = validate_date_format(start_date, "Start Date")

        end_date = input("Enter project end date (YYYY-MM-DD): ")
        end_date = validate_required(end_date, "End Date")
        end_date = validate_date_format(end_date, "End Date")

        start_date, end_date = validate_start_end_dates(start_date, end_date)
        new_project["start_date"] = start_date
        new_project["end_date"] = end_date

        owner_email = database.current_user["email"]
        new_project["owner_email"] = owner_email

        database.add_project(new_project)
        print("Project created successfully!")

    except ValueError as e:
        print(f"Error: {e}")


def view_all_projects():
    print("\n=== All Projects ===")
    projects = database.get_projects()
    if not projects:
        print("No projects found.")
        return

    for idx, project in enumerate(projects, start=1):
        print_project(project, idx)


def view_my_projects():
    print("\n=== My Projects ===")
    if database.current_user is None:
        print("You must be logged in to view your projects.")
        return

    projects = get_current_user_projects(database.get_projects())

    if not projects:
        print("You have not created any projects yet.")
        return

    for idx, project in enumerate(projects, start=1):
        print_project(project, idx, False)


def edit_project():
    if database.current_user is None:
        print("You must be logged in to edit your projects.")
        return

    data = database.load_data()
    projects = get_current_user_projects(data["projects"])

    if not projects:
        print("You have not created any projects yet.")
        return

    print("\n=== Own projects ===")
    for idx, project in enumerate(projects, start=1):
        print(f"{idx}. {project['title']}")

    choice = input("Enter the number of the project you want to edit: ")

    try:
        choice = validate_required(choice, "Project Choice")
        choice = validate_choice(choice, range(1, len(projects) + 1))
        project_to_edit = projects[choice - 1]

        new_title = input(
            f"Enter new title (leave blank to keep '{project_to_edit['title']}'): "
        )
        new_details = input("Enter new details (leave blank to keep current details): ")
        new_target = input(
            f"Enter new total target (leave blank to keep '{project_to_edit['total_target']}'): "
        )
        new_start_date = input(
            f"Enter new start date (YYYY-MM-DD) (leave blank to keep '{project_to_edit['start_date']}'): "
        )
        new_end_date = input(
            f"Enter new end date (YYYY-MM-DD) (leave blank to keep '{project_to_edit['end_date']}'): "
        )

        final_title = new_title.strip() or project_to_edit["title"]
        final_title = validate_required(final_title, "Project Title")

        final_details = new_details.strip() or project_to_edit["details"]
        final_details = validate_required(final_details, "Project Details")

        final_target = new_target.strip() or str(project_to_edit["total_target"])
        final_target = validate_positive_number(final_target, "Total Target")

        final_start_date = new_start_date.strip() or project_to_edit["start_date"]
        final_start_date = validate_date_format(final_start_date, "Start Date")

        final_end_date = new_end_date.strip() or project_to_edit["end_date"]
        final_end_date = validate_date_format(final_end_date, "End Date")
        final_start_date, final_end_date = validate_start_end_dates(
            final_start_date,
            final_end_date,
        )

        project_to_edit["title"] = final_title
        project_to_edit["details"] = final_details
        project_to_edit["total_target"] = final_target
        project_to_edit["start_date"] = final_start_date
        project_to_edit["end_date"] = final_end_date

        database.save_data(data)
        print("Project updated successfully!")
    except ValueError as e:
        print(f"Error: {e}")


def delete_project():
    if database.current_user is None:
        print("You must be logged in to delete your projects.")
        return

    data = database.load_data()
    projects = get_current_user_projects(data["projects"])

    if not projects:
        print("You have not created any projects yet.")
        return

    print("\n=== Own projects ===")
    for idx, project in enumerate(projects, start=1):
        print(f"{idx}. {project['title']}")

    choice = input("Enter the number of the project you want to delete: ")
    try:
        choice = validate_required(choice, "Project Choice")
        choice = validate_choice(choice, range(1, len(projects) + 1))
        project_to_delete = projects[choice - 1]

        data["projects"].remove(project_to_delete)
        database.save_data(data)
        print("Project deleted successfully!")
    except ValueError as e:
        print(f"Error: {e}")


def search_projects_by_date():
    print("\n=== Search Projects By Date ===")
    date_input = input("Enter a date (YYYY-MM-DD) to find active projects: ")
    try:
        date_input = validate_required(date_input, "Date")
        date_input = validate_date_format(date_input, "Date")

        projects = database.get_projects()
        active_projects = [
            p for p in projects if p["start_date"] <= date_input <= p["end_date"]
        ]

        if not active_projects:
            print("No active projects found for the given date.")
            return

        print(f"\nProjects active on {date_input}:")
        for idx, project in enumerate(active_projects, start=1):
            print_project(project, idx)

    except ValueError as e:
        print(f"Error: {e}")
