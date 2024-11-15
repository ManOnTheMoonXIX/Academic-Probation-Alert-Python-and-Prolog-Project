% Defining the default GPA (2.0)
% This predicate establishes a default GPA value. It can be used to compare students' GPAs against this standard.
default_gpa(2.0).

% Grade mapping from letter grades to grade points
% These predicates map letter grades to their corresponding grade points. 
% This is essential for calculating GPAs based on the letter grades received by students.
letter_grade_to_points('A+', 4.3).
letter_grade_to_points('A', 4.0).
letter_grade_to_points('A-', 3.7).
letter_grade_to_points('B+', 3.3).
letter_grade_to_points('B', 3.0).
letter_grade_to_points('B-', 2.7).
letter_grade_to_points('C+', 2.3).
letter_grade_to_points('C', 2.0).
letter_grade_to_points('C-', 1.7).
letter_grade_to_points('D+', 1.3).
letter_grade_to_points('D', 1.0).
letter_grade_to_points('F', 0.0).

% Student data (Student ID, Student Name, Email, School, Programme)
% This set of predicates holds information about students, including their ID, name, email, school, and academic program.
student_data(1234567, 'Justin Alder', 'justin.alder@gmail.com', 'School of Engineering', 'Computer Science').
student_data(2345678, 'Briana Taylor', 'briana.taylor@gmail.com', 'School of Engineering', 'Computer Science').
student_data(3456789, 'Daryn Brown', 'daryn.brown@gmail.com', 'School of Engineering', 'Computer Science').
student_data(4567890, 'Marvis Haughton', 'marvis.haughton@gmail.com', 'School of Engineering', 'Computer Science').
student_data(5678901, 'Emily Chen', 'emily.chen@gmail.com', 'School of Engineering', 'Computer Science').
student_data(6789012, 'Michael Lee', 'michael.lee@gmail.com', 'School of Engineering', 'Computer Science').
student_data(7890123, 'Sarah Kim', 'sarah.kim@gmail.com', 'School of Engineering', 'Computer Science').
student_data(8901234, 'David Park', 'david.park@gmail.com', 'School of Engineering', 'Computer Science').

% Module data (Module ID, Module Name, Credits)
% These predicates provide information about the modules (courses) offered, including their ID, name, and credit value.
module_data('MAT2003', 'Calculus 1', 3).
module_data('CMP4011', 'Artificial Intelligence', 4).
module_data('CIT3009', 'Advanced Programming', 4).
module_data('CIT2011', 'Web Programming', 3).
module_data('PSY1002', 'Introduction to Psychology', 3).
module_data('ENT3001', 'Entrepreneurship', 3).
module_data('COM1024', 'Academic Literacy for Undergraduates', 3).
module_data('MAT1043', 'Linear Algebra', 3).
module_data('STA2020', 'Introductory Statistics', 3).
module_data('CIT4024', 'IT Project Management', 4).

% Module Details (Student ID, Module ID, Academic Year, Semester, LetterGrade)
% This set of predicates records the specific modules taken by each student, along with their grades for each module in a given semester.
module_details(1234567, 'MAT2003', '2023/2024', 1, 'A+').
module_details(1234567, 'CMP4011', '2023/2024', 1, 'B+').
module_details(1234567, 'CIT3009', '2023/2024', 2, 'C+').
module_details(2345678, 'MAT2003', '2023/2024', 1, 'D+').
module_details(2345678, 'CIT2011', '2023/2024', 1, 'F').
module_details(2345678, 'PSY1002', '2023/2024', 2, 'A-').
module_details(2345678, 'MAT2003', '2024/2025', 1, 'C+').
module_details(2345678, 'CIT2011', '2024/2025', 1, 'A').
module_details(2345678, 'PSY1002', '2024/2025', 2, 'A-').
module_details(3456789, 'ENT3001', '2023/2024', 1, 'B-').
module_details(3456789, 'COM1024', '2023/2024', 1, 'C-').
module_details(4567890, 'MAT1043', '2023/2024', 1, 'D-').
module_details(4567890, 'STA2020', '2023/2024', 2, 'F').
module_details(5678901, 'MAT2003', '2023/2024', 1, 'A+').
module_details(5678901, 'CMP4011', '2023/2024', 1, 'B+').
module_details(5678901, 'CIT3009', '2023/2024', 2, 'C+').
module_details(6789012, 'MAT2003', '2023/2024', 1, 'D+').
module_details(6789012, 'CIT2011', '2023/2024', 1, 'F').
module_details(6789012, 'PSY1002', '2023/2024', 2, 'A-').
module_details(7890123, 'ENT3001', '2023/2024', 1, 'B-').
module_details(7890123, 'COM1024', '2023/2024', 1, 'C-').
module_details(8901234, 'MAT1043', '2023/2024', 1, 'D-').
module_details(8901234, 'STA2020', '2023/2024', 2, 'F').

% Ascertain the total credit for the modules taken by the student for each semester and year
% This predicate calculates the total credits for a specific student in a given academic year and semester.
% It uses findall to gather all credit values for the modules the student is enrolled in during that semester.
semester_credits(StudentID, Academic_Year, Semester, Credits) :- 
    findall(
        Credit,
        (
            module_details(StudentID, ModuleID, Academic_Year, Semester, _),
            module_data(ModuleID, _, Credit)
        ),
        CreditsList
    ),
    sum_list(CreditsList, Credits). % Sums the list of credits to get the total.

% Calculate GPA for a given student, year, and semester
% This predicate computes the GPA for a student based on their grades and the credits of the modules taken.
% It retrieves the grade points and credits for each module, sums them, and divides by the total credits.
calculate_gpa(StudentID, Academic_Year, Semester, GPA) :-
    findall(GradePoints * Credits, (
        module_details(StudentID, ModuleID, Academic_Year, Semester, LetterGrade),
        letter_grade_to_points(LetterGrade, GradePoints),
        module_data(ModuleID, _, Credits)
    ), GradePointsList),
    sum_list(GradePointsList, TotalGradePoints), % Total grade points earned.
    semester_credits(StudentID, Academic_Year, Semester, TotalCredits), % Total credits taken.
    (TotalCredits > 0 -> GPA is TotalGradePoints / TotalCredits ; GPA is 0). % Calculate GPA or set to 0 if no credits.

% Calculate cumulative GPA for a student
% This predicate calculates the cumulative GPA across two semesters for a given academic year.
% It calls calculate_gpa for both semesters and combines the results based on the credits taken.
calculate_cumulative_gpa(StudentID, Academic_Year, CumulativeGPA) :-
    calculate_gpa(StudentID, Academic_Year, 1, GPA1), % GPA for first semester.
    calculate_gpa(StudentID, Academic_Year, 2, GPA2), % GPA for second semester.
    semester_credits(StudentID, Academic_Year, 1, Credits1), % Credits for first semester.
    semester_credits(StudentID, Academic_Year, 2, Credits2), % Credits for second semester.
    (Credits2 == 0 -> 
        CumulativeGPA is GPA1 ; % If no credits in second semester, use first semester GPA.
        CumulativeGPA is (GPA1 * Credits1 + GPA2 * Credits2) / (Credits1 + Credits2) % Weighted average of GPAs.
    ).

% Check if a student is on academic probation
% This predicate determines if a student is on academic probation by comparing their cumulative GPA to the default GPA.
on_academic_probation(StudentID) :-
    calculate_cumulative_gpa(StudentID, _, CumulativeGPA), % Calculate cumulative GPA.
    default_gpa(DefaultGPA), % Retrieve the default GPA.
    CumulativeGPA =< DefaultGPA. % Check if cumulative GPA is less than or equal to default.

% Update the default GPA
% This predicate allows for updating the default GPA value in the system.
% It retracts the old default GPA and asserts the new one.
update_default_gpa(NewGPA) :-
    retract(default_gpa(_)), % Remove the existing default GPA.
    assert(default_gpa(NewGPA)). % Set the new default GPA.
