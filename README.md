# Crowdfunding Console Application

A simple console-based crowdfunding application built with Python.

## Features

- User registration
- Account activation
- User login and logout
- Create project
- View all projects
- View my projects
- Edit my projects
- Delete my projects
- Search projects by date

## Project Files

- `main.py` : application entry point
- `auth.py` : authentication logic
- `project.py` : project logic
- `utils.py` : validation functions
- `database.py` : JSON storage functions
- `data.json` : saved users and projects

## Validation

- Email format validation
- Egyptian phone number validation
- Password confirmation
- Positive target validation
- Date format validation
- Start date must be before end date

## Storage

- Users and projects are stored in `data.json`
- Logged-in user is stored temporarily during app runtime

## Run

Use:

```powershell
py main.py
```

## Notes

- Passwords are stored as plain text for learning purposes
- This project uses JSON instead of a real database
