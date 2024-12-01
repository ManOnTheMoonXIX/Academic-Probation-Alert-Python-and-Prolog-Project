from pyswip import Prolog
from gui_app import AcademicProbationApp
from db_connection import (
    get_student_data,
    get_module_data,
    close_connection,
    populate_module_details,
    get_missing_semester_data, 
    update_semester_data
)
from email.mime.text import MIMEText
import smtplib

# Initialize Prolog engine
prolog = Prolog()
prolog.consult("gpacalc.pl")  # Ensure this matches the path to your Prolog file

def query_prolog(query_str):
    """Helper function to query Prolog safely."""
    try:
        return list(prolog.query(query_str))  # Ensure all results are returned as a list
    except Exception as e:
        print(f"Error in Prolog query '{query_str}': {e}")
        return []

def get_student_gpa(student_id, semester):
    """Retrieve the GPA of a student for a specific semester."""
    result = query_prolog(f"calculate_gpa({student_id}, '2023/2024', {semester}, GPA)")
    return result[0]['GPA'] if result else 0

def get_cumulative_gpa(student_id, year):
    """Retrieve the cumulative GPA of a student for the given year."""
    result = query_prolog(f"calculate_cumulative_gpa({student_id}, '{year}', CumulativeGPA)")
    return result[0]['CumulativeGPA'] if result else 0

def is_on_academic_probation(student_id):
    """Check if a student is on academic probation."""
    result = query_prolog(f"on_academic_probation({student_id})")
    return bool(result)

def ensure_semester_data():
    """Check for missing semester data and populate it dynamically."""
    missing_rows = get_missing_semester_data()  # Use the function to fetch missing rows

    for row in missing_rows:
        record_id, student_id, module_id, academic_year, letter_grade = row

        # Example logic to assign semester (adjust as needed)
        semester = 1 if "CMP" in module_id or "MAT" in module_id else 2

        # Update the database with the missing semester value
        update_semester_data(record_id, semester)

def populate_prolog_from_db():
    """Populate Prolog facts dynamically from the MySQL database."""
    # Clear existing Prolog facts to avoid duplication
    prolog.retractall("student_data(_, _, _, _, _)")
    prolog.retractall("module_data(_, _, _)")
    prolog.retractall("module_details(_, _, _, _, _)")

    # Load students
    students = get_student_data()
    for student in students:
        student_id, name, email, school, programme = student
        prolog.assertz(f"student_data({student_id}, '{name}', '{email}', '{school}', '{programme}')")

    # Load modules and module details for both semesters
    for student in students:
        student_id = student[0]

        # Load Semester 1 data
        modules_sem1 = get_module_data(student_id, "2023/2024", 1)  # Adjust academic year and semester
        for module_id, module_name, letter_grade, credits in modules_sem1:
            prolog.assertz(f"module_data('{module_id}', '{module_name}', {credits})")
            prolog.assertz(f"module_details({student_id}, '{module_id}', '2023/2024', 1, '{letter_grade}')")

        # Load Semester 2 data
        modules_sem2 = get_module_data(student_id, "2023/2024", 2)  # Adjust academic year and semester
        for module_id, module_name, letter_grade, credits in modules_sem2:
            prolog.assertz(f"module_data('{module_id}', '{module_name}', {credits})")
            prolog.assertz(f"module_details({student_id}, '{module_id}', '2023/2024', 2, '{letter_grade}')")


def send_email_alert(student_id, name, email, programme, school="School of Engineering"):
    """Send academic probation alert emails to multiple stakeholders."""
    subject = "Academic Probation Alert"
    body = (
        f"Dear {name},\n\n"
        f"Your cumulative GPA has fallen below the threshold. Please contact your advisor immediately.\n"
        f"Programme: {programme}\n"
        f"School: {school}\n\n"
        f"Thank you,\nUniversity Administration."
    )
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "admin@university.com"

    # Add recipients
    recipients = [
        email,  # Student email
        "advisor@university.com",
        "director@university.com",
        "admin@university.com"
    ]
    msg["To"] = ", ".join(recipients)

    try:
        with smtplib.SMTP("smtp.mailtrap.io", 2525, timeout=30) as server:  # Adjust SMTP settings as needed
            server.login("your_username", "your_password")  # Replace with real credentials
            server.sendmail(msg["From"], recipients, msg.as_string())
        print(f"Email alert sent to {email} and other stakeholders.")
    except Exception as e:
        print(f"Error sending email alert for {name} (ID: {student_id}): {e}")

def generate_reports(year):
    """Generate GPA reports and send alerts for students on academic probation."""
    # Populate Prolog facts
    populate_prolog_from_db()

    # Fetch all student data dynamically from Prolog
    students = query_prolog("student_data(StudentID, Name, Email, _, Programme)")
    if not students:
        print("No students found.")
        return

    for result in students:
        student_id = result["StudentID"]
        name = result["Name"]
        email = result["Email"]
        programme = result["Programme"]

        # Fetch GPA data
        gpa1 = get_student_gpa(student_id, 1)
        gpa2 = get_student_gpa(student_id, 2)
        cumulative_gpa = get_cumulative_gpa(student_id, year)

        # Print report
        print(f"\nReport for {name} (ID: {student_id})")
        print(f"GPA Semester 1: {gpa1}")
        print(f"GPA Semester 2: {gpa2}")
        print(f"Cumulative GPA: {cumulative_gpa}")

        # Check academic probation
        if is_on_academic_probation(student_id):
            print(f"Alert: {name} is on academic probation!")
            send_email_alert(student_id, name, email, programme)

def main():
    """Main entry point for the script."""
    try:
        ensure_semester_data()  # Populate missing semester data
        generate_reports("2023/2024")
    except Exception as e:
        print(f"Error in report generation: {e}")
    finally:
        close_connection()

if __name__ == "__main__":
    app = AcademicProbationApp(
        get_student_gpa=get_student_gpa,
        get_cumulative_gpa=get_cumulative_gpa,
        is_on_academic_probation=is_on_academic_probation,
        populate_prolog_from_db=populate_prolog_from_db,
        query_prolog=query_prolog,
    )
    app.mainloop()
