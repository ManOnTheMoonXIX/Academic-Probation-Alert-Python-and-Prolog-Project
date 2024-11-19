import mysql.connector

# Establish the database connection
db = mysql.connector.connect(
    host="localhost",  # Change if your database host differs
    user="root",       # Replace with your database username
    password="password",  # Replace with your database password
    database="Academic_Probation"  # Replace with your database name
)

cursor = db.cursor()

# Fetch student data by student ID
def get_student_data(student_id=None):
    """Fetch student data. If student_id is provided, fetch for a specific student."""
    if student_id:
        query = "SELECT student_id, name, email, school, programme FROM students WHERE student_id = %s"
        cursor.execute(query, (student_id,))
    else:
        query = "SELECT student_id, name, email, school, programme FROM students"
        cursor.execute(query)
    return cursor.fetchall()

# Fetch module data for a specific student and academic year
def get_module_data(student_id, academic_year, semester):
    """Fetch module details for a specific student, academic year, and semester."""
    query = """
    SELECT md.module_id, m.module_name, md.letter_grade, m.credits
    FROM module_details md
    JOIN modules m ON md.module_id = m.module_id
    WHERE md.student_id = %s AND md.academic_year = %s AND md.semester = %s
    """
    cursor.execute(query, (student_id, academic_year, semester))
    return cursor.fetchall()

# Populate missing module details (for validation and testing)
def populate_module_details(student_id, module_id, academic_year, semester, letter_grade):
    """Insert data into the module_details table dynamically."""
    try:
        query = """
        INSERT INTO module_details (student_id, module_id, academic_year, semester, letter_grade)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (student_id, module_id, academic_year, semester, letter_grade))
        db.commit()
        print(f"Inserted data for student_id={student_id}, module_id={module_id}")
    except mysql.connector.Error as err:
        print(f"Error populating module_details: {err}")

# Update specific data in the database
def update_semester_data(record_id, semester):
    """Update the semester value for a specific record in the module_details table."""
    try:
        query = "UPDATE module_details SET semester = %s WHERE id = %s"
        cursor.execute(query, (semester, record_id))
        db.commit()
        print(f"Updated semester for record ID {record_id}: Semester={semester}")
    except mysql.connector.Error as err:
        print(f"Error updating semester data: {err}")

# Close the database connection
def close_connection():
    """Close the database connection."""
    cursor.close()
    db.close()

# Fetch all records with missing semester values
def get_missing_semester_data():
    """Fetch all records from module_details where the semester is missing."""
    query = "SELECT id, student_id, module_id, academic_year, letter_grade FROM module_details WHERE semester IS NULL"
    cursor.execute(query)
    return cursor.fetchall()
