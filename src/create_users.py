from db_connection import db, cursor
import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_user_for_all_students():
    try:
        # Fetch all existing students
        cursor.execute("SELECT student_id, email FROM students")
        students = cursor.fetchall()

        for student_id, email in students:
            # Hash the student ID as the password
            hashed_password = hash_password(str(student_id))

            # Insert the user record
            create_user_query = """
            INSERT INTO users (username, password_hash, role, student_id)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(create_user_query, (email, hashed_password, 'student', student_id))
        
        # Commit all changes
        db.commit()
        print("User accounts created for all students.")

    except Exception as e:
        print(f"Error creating user accounts: {e}")
        db.rollback()

if __name__ == "__main__":
    create_user_for_all_students()
