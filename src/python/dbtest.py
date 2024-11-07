import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="your_database"
)

cursor = conn.cursor()

# Run test queries
queries = {
    "Semester GPA": """
        SELECT student_id, SUM(grade_points * credits) / SUM(credits) AS gpa
        FROM ModuleDetails
        JOIN Module ON ModuleDetails.module_id = Module.module_id
        WHERE student_id = 1234567 AND semester = 1
        GROUP BY student_id;
    """,
    "Cumulative GPA": """
        SELECT student_id, SUM(grade_points * credits) / SUM(credits) AS cumulative_gpa
        FROM ModuleDetails
        JOIN Module ON ModuleDetails.module_id = Module.module_id
        WHERE student_id = 1234567
        GROUP BY student_id;
    """,
    "Academic Probation": """
        SELECT student_id, student_name, SUM(grade_points * credits) / SUM(credits) AS cumulative_gpa
        FROM ModuleDetails
        JOIN Module ON ModuleDetails.module_id = Module.module_id
        JOIN Student ON ModuleDetails.student_id = Student.student_id
        GROUP BY student_id
        HAVING cumulative_gpa <= 2.0;
    """
}

# Execute and print results
for description, query in queries.items():
    cursor.execute(query)
    print(f"{description} Results:")
    for row in cursor.fetchall():
        print(row)
    print()

cursor.close()
conn.close()
