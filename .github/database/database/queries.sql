-- Query 1: Active & Overdue Loans with Multi-table JOIN
SELECT i.id AS issue_id, s.name AS student_name, b.title AS book_title, i.issue_date, i.due_date, i.status
FROM issues i
JOIN students s ON i.student_id = s.id
JOIN books b ON i.book_id = b.id
WHERE i.return_date IS NULL
ORDER BY i.due_date ASC;

-- Query 2: Category Aggregation & Borrowing Frequency
SELECT b.category, COUNT(DISTINCT b.id) AS distinct_titles, SUM(b.copies) AS total_inventory, COUNT(i.id) AS total_borrowed
FROM books b
LEFT JOIN issues i ON b.id = i.book_id
GROUP BY b.category
ORDER BY total_borrowed DESC;

-- Query 3: Outstanding Unpaid Fines per Student
SELECT s.id, s.name, s.status, COUNT(f.id) AS unpaid_fines_count, SUM(f.amount) AS total_fine_amount
FROM students s
JOIN fines f ON s.id = f.student_id
WHERE f.status = 'UNPAID'
GROUP BY s.id, s.name, s.status;
