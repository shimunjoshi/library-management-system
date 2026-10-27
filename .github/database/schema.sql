-- Library Management System: 3NF Database Schema
-- MCA1015 Lab Assignment 1

DROP TABLE IF EXISTS fines;
DROP TABLE IF EXISTS issues;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS students;

CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll_no TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    status TEXT CHECK(status IN ('ACTIVE', 'SUSPENDED')) DEFAULT 'ACTIVE',
    max_borrow_limit INTEGER DEFAULT 3
);

CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    isbn TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    category TEXT NOT NULL,
    copies INTEGER NOT NULL CHECK(copies >= 0)
);

CREATE TABLE issues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    issue_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,
    status TEXT CHECK(status IN ('ISSUED', 'RETURNED', 'OVERDUE')) DEFAULT 'ISSUED',
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE RESTRICT,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE RESTRICT
);

CREATE TABLE fines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    issue_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    amount REAL NOT NULL CHECK(amount >= 0),
    fine_date DATE DEFAULT (DATE('now')),
    status TEXT CHECK(status IN ('UNPAID', 'PAID')) DEFAULT 'UNPAID',
    FOREIGN KEY (issue_id) REFERENCES issues(id),
    FOREIGN KEY (student_id) REFERENCES students(id)
);
