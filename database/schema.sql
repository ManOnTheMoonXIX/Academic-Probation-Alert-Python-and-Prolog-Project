-- Create table for student master information
CREATE TABLE Student (
    student_id INT PRIMARY KEY,
    student_name VARCHAR(100),
    email VARCHAR(100),
    school VARCHAR(100),
    program VARCHAR(100)
);

-- Create table for module information
CREATE TABLE Module (
    module_id VARCHAR(10) PRIMARY KEY,
    module_name VARCHAR(100),
    credits INT
);

-- Create table for module details including grades
CREATE TABLE ModuleDetails (
    student_id INT,
    module_id VARCHAR(10),
    year INT,
    semester INT,
    grade_points DECIMAL(5, 2),
    FOREIGN KEY (student_id) REFERENCES Student(student_id),
    FOREIGN KEY (module_id) REFERENCES Module(module_id),
    PRIMARY KEY (student_id, module_id, year, semester)
);

-- Default GPA setting
INSERT INTO SystemSettings (setting_name, setting_value) VALUES ('default_gpa', '2.0');
