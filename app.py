from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "change-this-secret-key"
DB_PATH = Path(__file__).with_name("library.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                category TEXT DEFAULT '',
                quantity INTEGER NOT NULL DEFAULT 1 CHECK(quantity >= 0)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                student_number TEXT NOT NULL UNIQUE
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS issues (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                student_id INTEGER NOT NULL,
                issue_date TEXT NOT NULL DEFAULT (date('now')),
                due_date TEXT NOT NULL,
                return_date TEXT,
                FOREIGN KEY(book_id) REFERENCES books(id),
                FOREIGN KEY(student_id) REFERENCES students(id)
            )
        """)
        if conn.execute("SELECT COUNT(*) FROM books").fetchone()[0] == 0:
            conn.executemany(
                "INSERT INTO books(title, author, category, quantity) VALUES (?, ?, ?, ?)",
                [
                    ("The Alchemist", "Paulo Coelho", "Fiction", 4),
                    ("Wings of Fire", "A. P. J. Abdul Kalam", "Biography", 3),
                    ("Python Basics", "Programming Team", "Technology", 5),
                ],
            )
        if conn.execute("SELECT COUNT(*) FROM students").fetchone()[0] == 0:
            conn.executemany(
                "INSERT INTO students(name, student_number) VALUES (?, ?)",
                [("Aarav Sharma", "MCA001"), ("Riya Patel", "MCA002")],
            )


@app.route("/")
def index():
    with get_db() as conn:
        books = conn.execute("""
            SELECT b.*,
                   b.quantity - (
                     SELECT COUNT(*) FROM issues i
                     WHERE i.book_id = b.id AND i.return_date IS NULL
                   ) AS available
            FROM books b ORDER BY b.title
        """).fetchall()
        students = conn.execute("SELECT * FROM students ORDER BY name").fetchall()
        active_issues = conn.execute("""
            SELECT i.*, b.title AS book_title, s.name AS student_name,
                   CASE WHEN i.due_date < date('now') THEN 1 ELSE 0 END AS overdue
            FROM issues i
            JOIN books b ON b.id = i.book_id
            JOIN students s ON s.id = i.student_id
            WHERE i.return_date IS NULL
            ORDER BY i.due_date
        """).fetchall()
        stats = {
            "books": conn.execute("SELECT COUNT(*) FROM books").fetchone()[0],
            "students": conn.execute("SELECT COUNT(*) FROM students").fetchone()[0],
            "issued": conn.execute("SELECT COUNT(*) FROM issues WHERE return_date IS NULL").fetchone()[0],
        }
    return render_template("index.html", books=books, students=students,
                           active_issues=active_issues, stats=stats)


@app.post("/books/add")
def add_book():
    title = request.form.get("title", "").strip()
    author = request.form.get("author", "").strip()
    category = request.form.get("category", "").strip()
    try:
        quantity = int(request.form.get("quantity", "1"))
        if not title or not author or quantity < 0:
            raise ValueError
    except ValueError:
        flash("Enter a title, author, and a quantity of 0 or more.", "error")
        return redirect(url_for("index"))
    with get_db() as conn:
        conn.execute("INSERT INTO books(title, author, category, quantity) VALUES (?, ?, ?, ?)",
                     (title, author, category, quantity))
    flash("Book added successfully.", "success")
    return redirect(url_for("index"))


@app.post("/students/add")
def add_student():
    name = request.form.get("name", "").strip()
    number = request.form.get("student_number", "").strip()
    if not name or not number:
        flash("Enter both student name and student ID.", "error")
        return redirect(url_for("index"))
    try:
        with get_db() as conn:
            conn.execute("INSERT INTO students(name, student_number) VALUES (?, ?)", (name, number))
    except sqlite3.IntegrityError:
        flash("That student ID already exists.", "error")
        return redirect(url_for("index"))
    flash("Student added successfully.", "success")
    return redirect(url_for("index"))


@app.post("/issues/add")
def issue_book():
    try:
        book_id = int(request.form.get("book_id", ""))
        student_id = int(request.form.get("student_id", ""))
        due_date = request.form.get("due_date", "").strip()
        if not due_date:
            raise ValueError
    except ValueError:
        flash("Select a book, student, and due date.", "error")
        return redirect(url_for("index"))

    with get_db() as conn:
        book = conn.execute("""
            SELECT b.quantity - (
              SELECT COUNT(*) FROM issues i
              WHERE i.book_id = b.id AND i.return_date IS NULL
            ) AS available FROM books b WHERE b.id = ?
        """, (book_id,)).fetchone()
        student = conn.execute("SELECT id FROM students WHERE id = ?", (student_id,)).fetchone()
        if not book or book["available"] <= 0:
            flash("This book is not currently available.", "error")
        elif not student:
            flash("Select a valid student.", "error")
        else:
            conn.execute("INSERT INTO issues(book_id, student_id, due_date) VALUES (?, ?, ?)",
                         (book_id, student_id, due_date))
            flash("Book issued successfully.", "success")
    return redirect(url_for("index"))


@app.post("/issues/<int:issue_id>/return")
def return_book(issue_id):
    with get_db() as conn:
        result = conn.execute("""
            UPDATE issues SET return_date = date('now')
            WHERE id = ? AND return_date IS NULL
        """, (issue_id,))
        if result.rowcount:
            flash("Book returned successfully.", "success")
        else:
            flash("Active issue record not found.", "error")
    return redirect(url_for("index"))


@app.post("/books/<int:book_id>/delete")
def delete_book(book_id):
    with get_db() as conn:
        has_history = conn.execute("SELECT COUNT(*) FROM issues WHERE book_id = ?", (book_id,)).fetchone()[0]
        if has_history:
            flash("Cannot delete a book with issue history. Keep it for record accuracy.", "error")
        else:
            conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
            flash("Book deleted.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
