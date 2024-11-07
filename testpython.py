from pyswip import Prolog
import smtplib
from email.mime.text import MIMEText

# Initialize the Prolog engine
prolog = Prolog()
prolog.consult("gpa_calculator.pl")

def query_prolog(query_str):
    """Helper function to query Prolog safely."""
    return list(prolog.query(query_str))  # Ensure all results are returned as a list

def get_student_gpa(student_id, semester):
    """Retrieve the GPA of a student for a specific semester."""
    result = query_prolog(f"calculate_gpa({student_id}, {semester}, GPA)")
    return result[0]['GPA'] if result else None

def get_cumulative_gpa(student_id, year):
    """Retrieve the cumulative GPA of a student for the given year."""
    result = query_prolog(f"calculate_cumulative_gpa({student_id}, {year}, CumulativeGPA)")
    return result[0]['CumulativeGPA'] if result else None

def is_on_academic_probation(student_id, year):
    """Check if a student is on academic probation."""
    result = query_prolog(f"on_academic_probation({student_id}, {year})")
    return bool(result)

def send_email_alert(student_id, name, email, programme):
    """Send an academic probation alert email."""
    subject = "Academic Probation Alert"
    body = f"Dear {name},\n\nYour cumulative GPA has fallen below the threshold. Please contact your advisor.\n\nProgramme: {programme}"
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "admin@university.com"
    msg["To"] = email

    with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
        server.login("your_username", "your_password")
        server.sendmail("admin@university.com", email, msg.as_string())

def generate_reports(year):
    """Generate GPA reports and send alerts for students on academic probation."""
    students = query_prolog("student_data(StudentID, Name, Email, _, Programme)")
    if not students:
        print("No students found.")
        return

    for result in students:
        student_id = result["StudentID"]
        name = result["Name"]
        email = result["Email"]
        programme = result["Programme"]

        gpa1 = get_student_gpa(student_id, 1)
        gpa2 = get_student_gpa(student_id, 2)
        cumulative_gpa = get_cumulative_gpa(student_id, year)

        print(f"\nReport for {name} (ID: {student_id})")
        print(f"GPA Semester 1: {gpa1}")
        print(f"GPA Semester 2: {gpa2}")
        print(f"Cumulative GPA: {cumulative_gpa}")

        if is_on_academic_probation(student_id, year):
            print(f"Alert: {name} is on academic probation!")
            send_email_alert(student_id, name, email, programme)

# Run the report generation for the year 2023
generate_reports(2023)


