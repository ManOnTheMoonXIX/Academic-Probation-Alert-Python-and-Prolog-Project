% Allow runtime modification of predicates
:- dynamic student_data/5.
:- dynamic module_data/3.
:- dynamic module_details/5.
:- dynamic semester_gpa/4. % semester_gpa(StudentID, Academic_Year, Semester, GPA).
:- dynamic on_academic_probation/1.
:- dynamic default_gpa/1.


% Defining the default GPA (2.0)
default_gpa(2.0).

% Grade mapping from letter grades to grade points
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

% Example preloaded student data for testing (can be replaced dynamically)
student_data(1234567, 'Justin Alder', 'justin.alder@gmail.com', 'School of Engineering', 'Computer Science').
student_data(2345678, 'Briana Taylor', 'briana.taylor@gmail.com', 'School of Engineering', 'Computer Science').

% Example preloaded module data for testing
module_data('MAT2003', 'Calculus 1', 3).
module_data('CMP4011', 'Artificial Intelligence', 4).

% Example preloaded module details for testing
module_details(1234567, 'MAT2003', '2023/2024', 1, 'A+').
module_details(1234567, 'CMP4011', '2023/2024', 1, 'B+').

% Calculate total credits for a student in a semester
semester_credits(StudentID, Academic_Year, Semester, Credits) :- 
    findall(
        Credit,
        (
            module_details(StudentID, ModuleID, Academic_Year, Semester, _),
            module_data(ModuleID, _, Credit)
        ),
        CreditsList
    ),
    sum_list(CreditsList, Credits).

% Calculate GPA for a given student, academic year, and semester
calculate_gpa(StudentID, Academic_Year, Semester, GPA) :-
    findall(GradePoints * Credits, (
        module_details(StudentID, ModuleID, Academic_Year, Semester, LetterGrade),
        letter_grade_to_points(LetterGrade, GradePoints),
        module_data(ModuleID, _, Credits)
    ), GradePointsList),
    sum_list(GradePointsList, TotalGradePoints),
    semester_credits(StudentID, Academic_Year, Semester, TotalCredits),
    (TotalCredits > 0 -> GPA is TotalGradePoints / TotalCredits ; GPA is 0).

% Calculate cumulative GPA for a student
calculate_cumulative_gpa(StudentID, Academic_Year, CumulativeGPA) :-
    calculate_gpa(StudentID, Academic_Year, 1, GPA1),
    calculate_gpa(StudentID, Academic_Year, 2, GPA2),
    semester_credits(StudentID, Academic_Year, 1, Credits1),
    semester_credits(StudentID, Academic_Year, 2, Credits2),
    (Credits2 == 0 -> 
        CumulativeGPA is GPA1 ;
        CumulativeGPA is ((GPA1 * Credits1) + (GPA2 * Credits2)) / (Credits1 + Credits2)
    ).

% Recalculate GPA for a specific semester
recalculate_semester_gpa(StudentID, Academic_Year, Semester) :-
    calculate_gpa(StudentID, Academic_Year, Semester, GPA),
    retractall(semester_gpa(StudentID, Academic_Year, Semester, _)),  % Only retract for the given semester
    assertz(semester_gpa(StudentID, Academic_Year, Semester, GPA)).  % Add updated GPA fact

% Recalculate cumulative GPA
recalculate_cumulative_gpa(StudentID, Academic_Year) :-
    calculate_cumulative_gpa(StudentID, Academic_Year, NewCumulativeGPA),
    retractall(student_gpa(StudentID, Academic_Year, _)),
    assert(student_gpa(StudentID, Academic_Year, NewCumulativeGPA)).



% Check if a student is on academic probation
on_academic_probation(StudentID) :-
    calculate_cumulative_gpa(StudentID, _, CumulativeGPA),
    default_gpa(DefaultGPA),
    CumulativeGPA =< DefaultGPA.

% Update the default GPA threshold and recalculate probation status for all students
update_default_gpa(NewGPA) :-
    retract(default_gpa(_)),
    assert(default_gpa(NewGPA)),
    recalculate_all_probation_statuses.

% Recalculate probation status for all students
recalculate_all_probation_statuses :-
    findall(StudentID, student_data(StudentID, _, _, _, _), StudentIDs),
    forall(member(StudentID, StudentIDs), recalculate_probation_status(StudentID)).

% Recalculate probation status for a specific student
recalculate_probation_status(StudentID) :-
    calculate_cumulative_gpa(StudentID, _, CumulativeGPA),
    default_gpa(DefaultGPA),
    (CumulativeGPA =< DefaultGPA ->
        assertz(on_academic_probation(StudentID));
        retractall(on_academic_probation(StudentID))
    ).
