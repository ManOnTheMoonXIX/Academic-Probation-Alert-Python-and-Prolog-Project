# Academic Probation Alert System

The Academic Probation Alert System is a hybrid application built with Python and Prolog to manage student academic records, calculate GPAs, and send alerts for students on academic probation. It features a GUI built with CustomTkinter, a MySQL database for data storage, and Prolog for GPA calculations and probation logic.

## Features

- **Student & Admin Interface**: A user-friendly GUI for students to view GPA reports and probation status, and for admins to manage student/module data and generate reports.
- **GPA Calculation**: Automated semester and cumulative GPA calculations using Prolog logic.
- **Academic Probation Alerts**: Email notifications sent to students and stakeholders when a student’s GPA falls below the threshold.
- **Database Management**: MySQL backend to store student, module, and grade data.
- **Dynamic Updates**: Real-time updates to GPA and probation status with Prolog integration.

## Getting Started

### Prerequisites

- Python 3.7+
- MySQL Server (e.g., MySQL Community Server)
- Prolog (SWI-Prolog recommended)
- Required Python packages: `mysql-connector-python`, `bcrypt`, `customtkinter`, `pyswip`, `pillow`, `smtplib`

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/Academic-Probation-Alert-Python-and-Prolog-Project.git
   cd Academic-Probation-Alert-Python-and-Prolog-Project
   ```
   
2. Install required Python packages:

   ```
   pip install mysql-connector-python bcrypt customtkinter pyswip pillow
   ```

3. Set up the MySQL database:
- Create a database named `Academic_Probation`.
- Run the SQL scripts provided in the code (e.g., table creation and seed data) to initialize the schema and populate sample data.

   Example commands in MySQL:
  
      CREATE DATABASE Academic_Probation;
      USE Academic_Probation;
      -- Paste and run the CREATE TABLE and INSERT statements from the code

4. Configure the database connection:
- Update `db_connection.py` with your MySQL credentials (host, user, password, database).

   Example:
   
     ```
     python
     db = mysql.connector.connect(
         host="localhost",
         user="your_username",
         password="your_password",
         database="Academic_Probation"
     )
     ```

5. Set up email credentials:
- Update `testpython.py` with your SMTP email credentials for sending alerts.

   Example:
   
      server.login("your_email@gmail.com", "your_app_password")
    
6. Ensure Prolog is installed and the `gpacalc.pl` file is in the project directory.

## Running The Application

1. Start the application:
   
   ```
   python testpython.py
   ```

2. The GUI will launch, allowing you to log in as a student or admin:
     - **Student Login**: Use student email and student ID as password `(e.g., justin.alder@gmail.com, 1234567)`.
     - **Admin Login**: Configure an admin user in the `users` table manually or extend the code to include admin creation.
  
## Usage

**Admin Features**
- **Add Students/Modules**: Input new student or module details via the GUI.
- **Manage Module Details**: Assign grades and update module records for students.
- **Generate Reports**: View semester and cumulative GPA reports for all students or individual students.
- **Send Alerts**: Automatically email students on academic probation.
- **Update GPA Threshold**: Modify the default GPA threshold (default: 2.0).

**Student Features**
- **View GPA Report**: Check semester and cumulative GPA.
- **Probation Status**: See if you’re on academic probation.

**Database Schema**
- `Student`: Stores student details (ID, name, email, school, program).
- `Module`: Stores module details (ID, name, credits).
- `ModuleDetails`: Links students to modules with grades, year, and semester.
- `users`: Stores login credentials (username, password hash, role, student ID).

## Prolog Logic

The system uses Prolog for GPA calculations and probation checks:
- `calculate_gpa/4`: Computes semester GPA based on grade points and credits.
- `calculate_cumulative_gpa/3`: Calculates cumulative GPA across semesters.
- `on_academic_probation/1`: Determines if a student’s GPA is below the threshold.

   Example Prolog queries:
      
      calculate_gpa(1234567, '2023/2024', 1, GPA).
      on_academic_probation(1234567).

## Project Structure

- `db_connection.py`: Database connection and CRUD operations.
- `gui_app.py`: CustomTkinter GUI implementation.
- `testpython.py`: Main script integrating Prolog, GUI, and email alerts.
- `gpacalc.pl`: Prolog logic for GPA and probation calculations.
- `logo.png`: Application logo (ensure this file exists or remove the reference).

## Group Members

- Briana Taylor 2345678
- Justin Alder 2007273
- Daryn Brown 2002414
- Marvis Haughton 1802529

## License

This project is licensed under the MIT License - see the LICENSE file for details.

   





   
