# Library Management System

A beginner-friendly MCA project built with **Python Flask, SQLite, HTML, CSS and JavaScript**.

## Features
- View, search, add and delete books
- Register students
- Issue books with due dates
- Record book returns
- See currently issued and overdue books
- Dashboard counts for book titles, students and active issues
- SQLite database created automatically with sample data

## Project structure
```text
library-management-system/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js
```

## Run locally (Windows / VS Code)
1. Install Python 3.10 or newer.
2. Open this folder in VS Code.
3. Open Terminal → New Terminal.
4. Create a virtual environment: `py -m venv .venv`
5. Activate it in PowerShell: `.\.venv\Scripts\Activate.ps1`
6. Install Flask: `python -m pip install -r requirements.txt`
7. Start the app: `python app.py`
8. Open `http://127.0.0.1:5000` in your browser.

The `library.db` database is created automatically when the app starts. Keep the terminal open while using the app.

## Notes
- This is an educational prototype, not a production-ready system.
- The demo has no authentication. Do not expose it publicly with real student data.
- Change `app.secret_key` before any real deployment.
- The dashboard's book count represents distinct book titles, not total physical copies.
