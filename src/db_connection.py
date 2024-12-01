import mysql.connector
import bcrypt

# Establish the database connection
db = mysql.connector.connect(
    host="localhost",  # Change if your database host differs
    user="root",       # Replace with your database username
    password="password",  # Replace with your database password
    database="Academic_Probation"  # Replace with your database name
)

cursor = db.cursor()


def authenticate_user(username, password):
    """
    Authenticate a user (student or admin) by username and password.

    Args:
        username (str): Username provided during login.
        password (str): Plaintext password provided during login.

    Returns:
        dict: A dictionary containing user details if authentication is successful, None otherwise.
    """
    try:
        # Fetch user details from the database
        query = "SELECT user_id, password_hash, role, student_id FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        if result:
            user_id, password_hash, role, student_id = result

            # Verify the password
            if bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
                return {
                    "user_id": user_id,
                    "role": role,
                    "student_id": student_id  # Will be None for admins
                }

        # Authentication failed
        return None
    except Exception as e:
        print(f"Error during authentication: {e}")
        return None


def create_user(username, password, role, student_id=None):
    """
    Create a new user in the database.

    Args:
        username (str): Username for the user.
        password (str): Plaintext password.
        role (str): Role of the user ('admin' or 'student').
        student_id (int, optional): Student ID for student users.
    """
    try:
        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insert the user into the database
        query = """
        INSERT INTO users (username, password_hash, role, student_id)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (username, hashed_password.decode('utf-8'), role, student_id))
        db.commit()
        print(f"User {username} created successfully.")
    except Exception as e:
        print(f"Error creating user: {e}")


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
