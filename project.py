import database
from utils import (
    validate_required,
    validate_positive_number,
    validate_date_format,
    validate_start_end_dates,
)


def show_project_menu():
    """Display the project menu placeholder."""
    print("\n=== Project Menu ===")
    print("1. Create Project")
    print("2. View My Projects")
    print("3. View All Projects")
    print("4. Edit Own Projects")
    print("5. Delete Own Projects")
    print("6. Back to Main Menu")


    choice = input("Enter your choice: ")

    match choice:
        case "1":
            create_project()
        case "2":
            print("Viewing your projects is currently not implemented.")
        case "3":
            view_all_projects()
        case "4":
            print("Editing projects is currently not implemented.")
        case "5":
            print("Deleting projects is currently not implemented.")
        case "6":
            print("Returning to the main menu.")
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
        print(f"\nProject #{idx}")
        print(f"Title: {project['title']}")
        print(f"Details: {project['details']}")
        print(f"Target: {project['total_target']}")
        print(f"Start Date: {project['start_date']}")
        print(f"End Date: {project['end_date']}")
        print(f"Owner: {project['owner_email']}")
        print("-" * 30)


    
