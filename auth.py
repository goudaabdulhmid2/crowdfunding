from utils import (
    validate_required,
    validate_email,
    validate_password_confirmation,
    validate_egyptian_phone,
    validate_email_is_unique,
)
import database

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
            activate_account()
        case "3":
            login()
        case "4":
            print("Exiting the application. Goodbye!")
        case _:
            print("Invalid choice. Please try again.")



def register_user():
    new_user = {}
    try:
        first_name = input("Enter your First Name: ")
        first_name = validate_required(first_name, "First Name")
        new_user["first_name"] = first_name

        last_name = input("Enter your Last Name: ")
        last_name = validate_required(last_name, "Last Name")
        new_user["last_name"] = last_name

        email = input("Enter your Email: ")
        email = validate_required(email, "Email")
        email = validate_email(email)
        email = validate_email_is_unique(email)
        new_user["email"] = email

        password = input("Enter your Password: ")
        password = validate_required(password, "Password")

        confirm_password = input("Confirm your Password: ")
        confirm_password = validate_required(confirm_password, "Confirm Password")
        validate_password_confirmation(password, confirm_password)
        new_user["password"] = password

        phone = input("Enter your Phone Number: ")
        phone = validate_required(phone, "Phone Number")
        phone = validate_egyptian_phone(phone)
        new_user["phone"] = phone

        new_user["is_active"] = False

        database.add_user(new_user)
        print("Registration successful! Please activate your account before logging in.")
    
    except ValueError as e:
        print(f"Error: {e}")


def activate_account():
    try:
        input_email = input("Enter your email to activate your account: ")
        input_email = validate_required(input_email, "Email")
        input_email = validate_email(input_email)

        data = database.load_data()

        for user in data["users"]:
            if user["email"] == input_email:
                if user["is_active"]:
                    print("Account is already active.")
                else:
                    user["is_active"] = True
                    database.save_data(data)
                    print("Account activated successfully!")
                return
        raise ValueError("Email not found. Please register first.")
    
    except ValueError as e:
        print(f"Error: {e}")


def login():
    try:
        input_email = input("Enter your email to login: ")
        input_email = validate_required(input_email, "Email")
        input_email = validate_email(input_email)

        input_password = input("Enter your password: ")
        input_password = validate_required(input_password, "Password")

        for user in database.get_users():
            if user["email"] == input_email:
                if not user["is_active"]:
                    print("Account is not active. Please activate your account first.")
                    return
                if user["password"] == input_password:
                    print(f"Welcome back, {user['first_name']}!")
                    database.current_user = user
                    return
                else:
                    raise ValueError("Incorrect password. Please try again.")
                
        raise ValueError("Email not found. Please register first.")

    except ValueError as e:
        print(f"Error: {e}")