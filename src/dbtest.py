from db_connection import get_student_data, get_module_data, calculate_gpa, close_connection

def test_database_connection():
    """Test database connection and basic queries."""
    try:
        print("Testing database connection...")

        # Test fetching all students
        print("\nFetching all student data...")
        students = get_student_data()
        for student in students:
            print(student)

        # Test fetching module details
        print("\nFetching module details for Student 1234567 in 2023/2024, Semester 1...")
        modules = get_module_data(1234567, "2023/2024", 1)
        for module in modules:
            print(module)

        # Test GPA calculation
        print("\nCalculating GPA for Student 1234567 in 2023/2024, Semester 1...")
        gpa = calculate_gpa(1234567, "2023/2024", 1)
        print(f"GPA: {gpa}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the connection
        close_connection()

if __name__ == "__main__":
    test_database_connection()
