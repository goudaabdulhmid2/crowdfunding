from utils import (
    validate_required,
    validate_email,
    validate_password_confirmation,
    validate_egyptian_phone,
    validate_email_is_unique,
)
from database import users


def show_auth_menu():
    print("\n=== Authentication Menu ===")
    print("1. Register")
    print("2. Activate Account")
    print("3. Login")
    print("4. Exit")

    choice = input("Enter your choice: ")

    match choice:
        case "1":
            register_user()
        case "2":
            print("Account activation is currently not implemented.")
        case "3":
            print("Login is currently not implemented.")
        case "4":
            print("Exiting the application. Goodbye!")
        case _:
            print("Invalid choice. Please try again.")



def register_user():
    new_user = {}
    try:
        first_name = input("Enter ur First Name: ")
        first_name = validate_required(first_name, "First Name")
        new_user["first_name"] = first_name

        last_name = input("Enter ur Last Name: ")
        last_name = validate_required(last_name, "Last Name")
        new_user["last_name"] = last_name

        email = input("Enter ur Email: ")
        email = validate_required(email, "Email")
        email = validate_email(email)
        email = validate_email_is_unique(email)
        new_user["email"] = email

        password = input("Enter ur Password: ")
        password = validate_required(password, "Password")

        confirm_password = input("Confirm ur Password: ")
        confirm_password = validate_required(confirm_password, "Confirm Password")
        validate_password_confirmation(password, confirm_password)
        new_user["password"] = password

        phone = input("Enter ur Phone Number: ")
        phone = validate_required(phone, "Phone Number")
        phone = validate_egyptian_phone(phone)
        new_user["phone"] = phone

        new_user["is_active"] = False

        users.append(new_user)
        print("Registration successful! Please activate your account before logging in.")
    
    except ValueError as e:
        print(f"Error: {e}")
