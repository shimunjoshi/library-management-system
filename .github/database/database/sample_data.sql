-- Seed Data for LMS Evaluation
INSERT INTO students (name, roll_no, email, status, max_borrow_limit) VALUES
('Aarav Sharma', 'MCA202601', 'aarav@avantika.edu.in', 'ACTIVE', 3),
('Diya Patel', 'MCA202602', 'diya@avantika.edu.in', 'ACTIVE', 3),
('Rohan Verma', 'MCA202603', 'rohan@avantika.edu.in', 'ACTIVE', 5),
('Ananya Iyer', 'MCA202604', 'ananya@avantika.edu.in', 'SUSPENDED', 3);

INSERT INTO books (isbn, title, author, category, copies) VALUES
('978-0132350884', 'Clean Code', 'Robert C. Martin', 'Software Engineering', 5),
('978-0201633610', 'Design Patterns', 'Erich Gamma et al.', 'Software Engineering', 4),
('978-0134685991', 'Effective Java', 'Joshua Bloch', 'Programming', 3),
('978-0262033848', 'Introduction to Algorithms', 'Thomas H. Cormen', 'Computer Science', 2);

INSERT INTO issues (book_id, student_id, issue_date, due_date, return_date, status) VALUES
(1, 1, '2026-10-01', '2026-10-15', '2026-10-14', 'RETURNED'),
(2, 1, '2026-10-10', '2026-10-24', NULL, 'OVERDUE'),
(1, 2, '2026-10-12', '2026-10-26', NULL, 'OVERDUE'),
(3, 3, '2026-10-20', '2026-11-03', NULL, 'ISSUED');

INSERT INTO fines (issue_id, student_id, amount, fine_date, status) VALUES
(2, 1, 30.00, '2026-10-25', 'UNPAID'),
(3, 2, 10.00, '2026-10-27', 'UNPAID');
