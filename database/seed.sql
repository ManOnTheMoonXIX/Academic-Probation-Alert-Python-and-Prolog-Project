-- seed.sql
INSERT INTO Student (student_id, student_name, email, school, program) VALUES
(1234567, 'Justin Alder', 'justin.alder@gmail.com', 'School of Engineering', 'Computer Science'),
(2345678, 'Briana Taylor', 'briana.taylor@gmail.com', 'School of Engineering', 'Computer Science');

INSERT INTO Module (module_id, module_name, credits) VALUES
('MAT2003', 'Calculus 1', 3),
('CMP4011', 'Artificial Intelligence', 4);

INSERT INTO ModuleDetails (student_id, module_id, year, semester, grade_points) VALUES
(1234567, 'MAT2003', 2023, 1, 80),
(1234567, 'CMP4011', 2023, 1, 90),
(2345678, 'MAT2003', 2023, 1, 70),
(2345678, 'CMP4011', 2023, 1, 60);
