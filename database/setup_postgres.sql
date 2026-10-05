
-- إنشاء الجداول وإدخال البيانات الأولية


DROP TABLE IF EXISTS enrollments CASCADE;
DROP TABLE IF EXISTS courses CASCADE;
DROP TABLE IF EXISTS academic_records CASCADE;

CREATE TABLE academic_records (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL UNIQUE,
    gpa NUMERIC(3, 2),
    attendance INTEGER,
    status VARCHAR(20),
    enrolled_date DATE DEFAULT CURRENT_DATE
);

CREATE TABLE courses (
    course_id INTEGER PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    credit_hours INTEGER
);

CREATE TABLE enrollments (
    enrollment_id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES academic_records(student_id),
    course_id INTEGER REFERENCES courses(course_id),
    semester VARCHAR(20),
    score NUMERIC(5, 2)
);

INSERT INTO courses (course_id, course_name, credit_hours) VALUES
    (1, 'Introduction to Programming', 3),
    (2, 'Data Structures', 4),
    (3, 'Database Systems', 3),
    (4, 'Machine Learning', 3),
    (5, 'Web Development', 3);


INSERT INTO academic_records (student_id, gpa, attendance, status) VALUES
    (1001, 3.45, 92, 'Active'),
    (1002, 3.80, 95, 'Active'),
    (1003, 2.90, 80, 'Active'),
    (1004, 3.10, 88, 'Active'),
    (1005, 2.50, 70, 'Active'),
    (1006, 3.95, 98, 'Active'),
    (1007, 5.00, 150, 'Active'),
    (1008, 2.20, 60, 'Active'),
    (1010, 3.30, 85, 'Active'),
    (1011, 3.60, 90, 'Active'),
    (1012, 1.80, 65, 'Active'),
    (1013, 3.20, 78, 'Active'),
    (1014, 3.75, 96, 'Active'),
    (1015, 2.85, 72, 'Active'),
    (1016, 3.55, 91, 'Active'),
    (1017, 3.90, 94, 'Active'),
    (1018, 3.15, 83, 'Active'),
    (1019, 2.70, 68, 'Active'),
    (1020, 3.65, 89, 'Active');

##
INSERT INTO enrollments (student_id, course_id, semester, score) VALUES
    (1001, 1, '2024-Fall', 85),
    (1001, 2, '2024-Fall', 90),
    (1002, 1, '2024-Fall', 95),
    (1002, 4, '2024-Spring', 88),
    (1003, 1, '2024-Fall', 70),
    (1003, 3, '2024-Fall', 75),
    (1004, 2, '2024-Fall', 80),
    (1004, 5, '2024-Spring', 85),
    (1005, 1, '2024-Fall', 60),
    (1006, 4, '2024-Fall', 98),
    (1008, 3, '2024-Fall', 55),
    (1010, 1, '2024-Fall', 88),
    (1011, 4, '2024-Fall', 92),
    (1012, 5, '2024-Fall', 65),
    (1013, 2, '2024-Fall', 82),
    (1014, 4, '2024-Fall', 96),
    (1015, 1, '2024-Fall', 78),
    (1016, 3, '2024-Fall', 88),
    (1017, 4, '2024-Spring', 93),
    (1018, 5, '2024-Fall', 86),
    (1019, 1, '2024-Fall', 72),
    (1020, 2, '2024-Fall', 89);

# تحقق 
SELECT 'academic_records' AS table_name, COUNT(*) AS rows FROM academic_records
UNION ALL
SELECT 'courses', COUNT(*) FROM courses
UNION ALL
SELECT 'enrollments', COUNT(*) FROM enrollments;