from db_connection import create_user

if __name__ == "__main__":
    # Create an admin user
    create_user(username="admin@university.com", password="admin123", role="admin")

    # Create a student user
    create_user(username="student123", password="student123", role="student", student_id=1234567)
