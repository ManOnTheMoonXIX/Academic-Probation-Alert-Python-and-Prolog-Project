% Defining the default GPA (2.0)
default_gpa(2.0).

% Student data (Student ID, Student Name, Email, School, Programme)
student_data(1234567, 'Justin Alder', 'justin.alder@gmail.com', 'School of Engineering', 'Computer Science').
student_data(2345678, 'Briana Taylor', 'briana.taylor@gmail.com', 'School of Engineering', 'Computer Science').
student_data(3456789, 'Daryn Brown', 'daryn.brown@gmail.com', 'School of Engineering', 'Computer Science').
student_data(4567890, 'Marvis Haughton', 'marvis.haughton@gmail.com', 'School of Engineering', 'Computer Science').
student_data(5678901, 'Emily Chen', 'emily.chen@gmail.com', 'School of Engineering', 'Computer Science').
student_data(6789012, 'Michael Lee', 'michael.lee@gmail.com', 'School of Engineering', 'Computer Science').
student_data(7890123, 'Sarah Kim', 'sarah.kim@gmail.com', 'School of Engineering', 'Computer Science').
student_data(8901234, 'David Park', 'david.park@gmail.com', 'School of Engineering', 'Computer Science').

% Module data (Module ID, Module Name, Credits)
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

% Module Details (Student ID, Module ID, Year, Semester, GradePoints)
module_details(1234567, 'MAT2003', 2023, 1, 80).
module_details(1234567, 'CMP4011', 2023, 1, 90).
module_details(1234567, 'CIT3009', 2024, 2, 85).
module_details(2345678, 'MAT2003', 2023, 1, 70).
module_details(2345678, 'CIT2011', 2023, 1, 80).
module_details(2345678, 'PSY1002', 2024, 2, 60).
module_details(3456789, 'ENT3001', 2023, 1, 80).
module_details(3456789, 'COM1024', 2023, 1, 85).
module_details(4567890, 'MAT1043', 2023, 1, 90).
module_details(4567890, 'STA2020', 2024, 2, 80).
module_details(5678901, 'MAT2003', 2023, 1, 75).
module_details(5678901, 'CMP4011', 2023, 1, 85).
module_details(5678901, 'CIT3009', 2024, 2, 70).
module_details(6789012, 'MAT2003', 2023, 1, 65).
module_details(6789012, 'CIT2011', 2023, 1, 75).
module_details(6789012, 'PSY1002', 2024, 2, 55).
module_details(7890123, 'ENT3001', 2023, 1, 80).
module_details(7890123, 'COM1024', 2023, 1, 85).
module_details(8901234, 'MAT1043', 2023, 1, 90).
module_details(8901234, 'STA2020', 2024, 2, 80).

% Ascertain the total credit for the modules taken by the student for each semester
semester_credits(StudentID, Semester, Credits) :- 
    findall(
        Credit,
        (
            module_details(StudentID, ModuleID, _, Semester, _),
            module_data(ModuleID, _, Credit)
        ),
        CreditsList
    ),
    sum_list(CreditsList, Credits).

% Calculate GPA for a given student and semester
calculate_gpa(StudentID, Semester, GPA) :-
    findall(
        GradePoints * Credits,
        (
            module_details(StudentID, ModuleID, _, Semester, GradePoints),
            module_data(ModuleID, _, Credits)
        ),
        GradePointsList
    ),
    sum_list(GradePointsList, TotalGradePoints),
    semester_credits(StudentID, Semester, TotalCredits),
    (TotalCredits > 0 -> GPA is TotalGradePoints / TotalCredits ; GPA is 0).

% Calculate cumulative GPA for a student
calculate_cumulative_gpa(StudentID, CumulativeGPA) :-
    calculate_gpa(StudentID, 1, GPA1),
    calculate_gpa(StudentID, 2, GPA2),
    semester_credits(StudentID, 1, Credits1),
    semester_credits(StudentID, 2, Credits2),
    (Credits2 = 0 -> 
        CumulativeGPA = GPA1 ; 
        CumulativeGPA is (GPA1 * Credits1 + GPA2 * Credits2) / (Credits1 + Credits2)
    ).

% Check if a student is on academic probation
on_academic_probation(StudentID) :-
    calculate_cumulative_gpa(StudentID, CumulativeGPA),
    default_gpa(DefaultGPA),
    CumulativeGPA =< DefaultGPA.

% Update the default GPA
update_default_gpa(NewGPA) :-
    retract(default_gpa(_)),
    assert(default_gpa(NewGPA)).