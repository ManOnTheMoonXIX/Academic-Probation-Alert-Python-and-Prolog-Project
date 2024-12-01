import customtkinter as ctk
from tkinter import ttk

# Initialize customtkinter
ctk.set_appearance_mode("System")  # Light or Dark mode
ctk.set_default_color_theme("blue")  # Theme colors

from db_connection import get_student_data, close_connection, cursor, db
# from email_alerts import send_email_alert  # Assuming you have this function in email_alerts.py



# Create the main app class
class AcademicProbationApp(ctk.CTk):
    def __init__(self, get_student_gpa, get_cumulative_gpa, is_on_academic_probation, populate_prolog_from_db, query_prolog, send_email_alert):
        super().__init__()

        # Store function references
        self.get_student_gpa = get_student_gpa
        self.get_cumulative_gpa = get_cumulative_gpa
        self.is_on_academic_probation = is_on_academic_probation
        self.populate_prolog_from_db = populate_prolog_from_db
        self.query_prolog = query_prolog 
        self.send_email_alert = send_email_alert

        # Window settings
        self.title("Academic Probation System")
        self.geometry("1200x800")

        # Start with the home screen
        self.show_home_screen()

    def show_home_screen(self):
        """Display the home screen with Student and Admin login options."""
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        # Add title
        title_label = ctk.CTkLabel(self, text="Academic Probation System", font=("Arial", 24))
        title_label.pack(pady=20)

        # Add buttons for Student and Admin login
        student_button = ctk.CTkButton(self, text="Student Login", command=self.show_student_login)
        student_button.pack(pady=20)

        admin_button = ctk.CTkButton(self, text="Admin Login", command=self.show_admin_login)
        admin_button.pack(pady=20)

    def show_student_login(self):
        """Display the student login screen."""
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        # Add title
        title_label = ctk.CTkLabel(self, text="Student Login", font=("Arial", 24))
        title_label.pack(pady=20)

        # Add student login fields
        username_label = ctk.CTkLabel(self, text="Student ID:")
        username_label.pack(pady=10)
        username_entry = ctk.CTkEntry(self)
        username_entry.pack(pady=10)

        password_label = ctk.CTkLabel(self, text="Password:")
        password_label.pack(pady=10)
        password_entry = ctk.CTkEntry(self, show="*")
        password_entry.pack(pady=10)

        # Add login button
        login_button = ctk.CTkButton(self, text="Login", command=lambda: self.authenticate_student(username_entry.get(), password_entry.get()))
        login_button.pack(pady=20)

        # Back button
        back_button = ctk.CTkButton(self, text="Back", command=self.show_home_screen)
        back_button.pack(pady=10)

    def show_admin_login(self):
        """Display the admin login screen."""
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        # Add title
        title_label = ctk.CTkLabel(self, text="Admin Login", font=("Arial", 24))
        title_label.pack(pady=20)

        # Add admin login fields
        username_label = ctk.CTkLabel(self, text="Username:")
        username_label.pack(pady=10)
        username_entry = ctk.CTkEntry(self)
        username_entry.pack(pady=10)

        password_label = ctk.CTkLabel(self, text="Password:")
        password_label.pack(pady=10)
        password_entry = ctk.CTkEntry(self, show="*")
        password_entry.pack(pady=10)

        # Add login button
        login_button = ctk.CTkButton(self, text="Login", command=lambda: self.authenticate_admin(username_entry.get(), password_entry.get()))
        login_button.pack(pady=20)

        # Back button
        back_button = ctk.CTkButton(self, text="Back", command=self.show_home_screen)
        back_button.pack(pady=10)

    def authenticate_student(self, username, password):
        """Authenticate a student."""
        from db_connection import authenticate_user  # Import the function

        user = authenticate_user(username, password)

        if user and user["role"] == "student":
            student_id = user["student_id"]
            print(f"Student {student_id} logged in successfully.")
            self.show_student_dashboard(student_id)
        else:
            ctk.CTkLabel(self, text="Invalid credentials for student login.", text_color="red").pack(pady=10)


    def authenticate_admin(self, username, password):
        """Authenticate an admin."""
        from db_connection import authenticate_user  # Import the function

        user = authenticate_user(username, password)

        if user and user["role"] == "admin":
            print(f"Admin {user['user_id']} logged in successfully.")
            self.show_admin_dashboard()
        else:
            ctk.CTkLabel(self, text="Invalid credentials for admin login.", text_color="red").pack(pady=10)


    def show_admin_dashboard(self):
        """Admin dashboard screen."""
        for widget in self.winfo_children():
            widget.destroy()

        title_label = ctk.CTkLabel(self, text="Admin Dashboard", font=("Arial", 24))
        title_label.pack(pady=20)

        # Button to generate GPA reports
        generate_reports_button = ctk.CTkButton(
            self, text="Generate GPA Reports",
            command=lambda: self.generate_gpa_reports("2023/2024")
        )
        generate_reports_button.pack(pady=10)

        # Button to update default GPA
        update_gpa_button = ctk.CTkButton(
            self, text="Update Default GPA",
            command=self.update_default_gpa
        )
        update_gpa_button.pack(pady=10)

        # Button to record/update GPA
        record_gpa_button = ctk.CTkButton(
            self, text="Record/Update GPA",
            command=self.record_gpa
        )
        record_gpa_button.pack(pady=10)

        # Button to generate individual student report
        generate_student_report_button = ctk.CTkButton(
            self, text="Generate Student Report",
            command=self.generate_report
        )
        generate_student_report_button.pack(pady=10)

        # Button to send alerts
        send_alerts_button = ctk.CTkButton(
            self, text="Send Alerts",
            command=self.send_alerts
        )
        send_alerts_button.pack(pady=10)

        # Button to add a new student
        add_student_button = ctk.CTkButton(
            self, text="Add New Student",
            command=self.show_add_student_screen
        )
        add_student_button.pack(pady=10)

        # Log out button
        back_button = ctk.CTkButton(self, text="Log Out", command=self.show_home_screen)
        back_button.pack(pady=20)


    def generate_gpa_reports(self, year):
        """Generate GPA reports using Prolog and display them in the GUI."""
        try:
            self.populate_prolog_from_db()  # Populate Prolog facts dynamically
            
            # Fetch all students from Prolog
            students = self.query_prolog("student_data(StudentID, Name, Email, School, Programme)")
            if not students:
                raise Exception("No students found in Prolog database.")
            
            # Clear the screen
            for widget in self.winfo_children():
                widget.destroy()

            # Add title
            title_label = ctk.CTkLabel(self, text=f"GPA Reports for {year}", font=("Arial", 24))
            title_label.pack(pady=20)

            # Create a frame for the table and scrollbar
            table_frame = ctk.CTkFrame(self)
            table_frame.pack(pady=10, padx=10, fill="both", expand=True)

            # Define custom styles for the Treeview
            style = ttk.Style()
            style.configure(
                "Custom.Treeview",
                background="blue",
                foreground="white",
                fieldbackground="blue",
                font=("Arial", 14),  # Larger font
                rowheight=30,  # Increase row height for better visibility
            )
            style.configure(
                "Custom.Treeview.Heading",
                font=("Arial Bold", 16),  # Larger, bold font for headings
                background="darkblue",
                foreground="white",
            )
            style.map(
                "Custom.Treeview",
                background=[("selected", "darkblue")],
                foreground=[("selected", "white")],
            )

            # Define table columns
            columns = ("Student ID", "Name", "Email", "School", "Programme", "GPA Semester 1", "GPA Semester 2", "Cumulative GPA", "Probation Status")
            gpa_table = ttk.Treeview(table_frame, columns=columns, show="headings")

            # Set up column headings
            for col in columns:
                gpa_table.heading(col, text=col)
                gpa_table.column(col, anchor="center", width=150)

            # Add a vertical scrollbar
            scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=gpa_table.yview)
            gpa_table.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")
            gpa_table.pack(fill="both", expand=True)

            # Iterate through each student and calculate GPA using Prolog
            for student in students:
                student_id = student["StudentID"]
                name = student["Name"]
                email = student["Email"]
                school = student["School"]
                programme = student["Programme"]

                # Calculate semester GPAs
                gpa_sem1 = self.get_student_gpa(student_id, 1)
                gpa_sem2 = self.get_student_gpa(student_id, 2)

                # Calculate cumulative GPA
                cumulative_gpa = self.get_cumulative_gpa(student_id, year)

                # Determine probation status
                probation_status = "Yes" if self.is_on_academic_probation(student_id) else "No"

                # Insert data into the table
                gpa_table.insert("", "end", values=(
                    student_id, name, email, school, programme, f"{gpa_sem1:.2f}", f"{gpa_sem2:.2f}", f"{cumulative_gpa:.2f}", probation_status
                ))

            # Back button
            back_button = ctk.CTkButton(self, text="Back", command=self.show_admin_dashboard)
            back_button.pack(pady=20)
        except Exception as e:
            print(f"Error: {e}")
            ctk.CTkLabel(self, text="Error generating GPA reports.", text_color="red").pack(pady=20)


    def update_default_gpa(self):
        """Update the default GPA threshold."""
        for widget in self.winfo_children():
            widget.destroy()

        title_label = ctk.CTkLabel(self, text="Update Default GPA", font=("Arial", 24))
        title_label.pack(pady=20)

        gpa_label = ctk.CTkLabel(self, text="Enter new default GPA:")
        gpa_label.pack(pady=10)
        gpa_entry = ctk.CTkEntry(self)
        gpa_entry.pack(pady=10)

        submit_button = ctk.CTkButton(
            self, text="Submit",
            command=lambda: self.submit_default_gpa(gpa_entry.get())
        )
        submit_button.pack(pady=20)

        back_button = ctk.CTkButton(self, text="Back", command=self.show_admin_dashboard)
        back_button.pack(pady=20)

    def submit_default_gpa(self, gpa):
        """Submit the new default GPA to Prolog."""
        try:
            self.query_prolog(f"update_default_gpa({float(gpa)})")
            ctk.CTkLabel(self, text="Default GPA updated successfully!", text_color="green").pack(pady=20)
        except Exception as e:
            print(f"Error: {e}")
            ctk.CTkLabel(self, text="Error updating default GPA.", text_color="red").pack(pady=20)

    def record_gpa(self):
        """Screen to record/update GPA."""
        for widget in self.winfo_children():
            widget.destroy()

        title_label = ctk.CTkLabel(self, text="Record or Update GPA", font=("Arial", 24))
        title_label.pack(pady=20)

        student_id_label = ctk.CTkLabel(self, text="Student ID:")
        student_id_label.pack(pady=10)
        student_id_entry = ctk.CTkEntry(self)
        student_id_entry.pack(pady=10)

        gpa_label = ctk.CTkLabel(self, text="GPA (Optional):")
        gpa_label.pack(pady=10)
        gpa_entry = ctk.CTkEntry(self)
        gpa_entry.pack(pady=10)

        submit_button = ctk.CTkButton(
            self, text="Submit", command=lambda: self.submit_gpa(student_id_entry.get(), gpa_entry.get())
        )
        submit_button.pack(pady=20)

        back_button = ctk.CTkButton(self, text="Back", command=self.show_admin_dashboard)
        back_button.pack(pady=10)

    def submit_gpa(self, student_id, gpa):
        """Submit GPA to the database."""
        try:
            if gpa:
                query = "UPDATE students SET gpa = %s WHERE student_id = %s"
                cursor.execute(query, (float(gpa), student_id))
                db.commit()
                ctk.CTkLabel(self, text="GPA updated successfully!", text_color="green").pack(pady=10)
            else:
                ctk.CTkLabel(self, text="Please enter a valid GPA.", text_color="red").pack(pady=10)
        except Exception as e:
            print(f"Error: {e}")
            ctk.CTkLabel(self, text="Error updating GPA.", text_color="red").pack(pady=10)

    def generate_report(self):
        """Screen to generate GPA reports."""
        for widget in self.winfo_children():
            widget.destroy()

        title_label = ctk.CTkLabel(self, text="Generate GPA Report", font=("Arial", 24))
        title_label.pack(pady=20)

        student_id_label = ctk.CTkLabel(self, text="Student ID:")
        student_id_label.pack(pady=10)
        student_id_entry = ctk.CTkEntry(self)
        student_id_entry.pack(pady=10)

        submit_button = ctk.CTkButton(
            self, text="Generate", command=lambda: self.display_report(student_id_entry.get())
        )
        submit_button.pack(pady=20)

        back_button = ctk.CTkButton(self, text="Back", command=self.show_admin_dashboard)
        back_button.pack(pady=10)

    def display_report(self, student_id):
        """Fetch and display the GPA report for the student."""
        try:
            query = """
            SELECT student_id, name, email, school, programme
            FROM students WHERE student_id = %s
            """
            cursor.execute(query, (student_id,))
            result = cursor.fetchone()

            if result:
                report = f"""
                Student ID: {result[0]}
                Name: {result[1]}
                Email: {result[2]}
                School: {result[3]}
                Programme: {result[4]}
                """
                ctk.CTkLabel(self, text=report, text_color="black", wraplength=500).pack(pady=20)
            else:
                ctk.CTkLabel(self, text="Student not found.", text_color="red").pack(pady=10)
        except Exception as e:
            print(f"Error: {e}")
            ctk.CTkLabel(self, text="Error generating report.", text_color="red").pack(pady=10)

    def send_alerts(self):
        """Send alerts to students whose cumulative GPA is below the threshold."""
        try:
            # Fetch all student data
            self.populate_prolog_from_db()  # Ensure Prolog facts are updated
            students = self.query_prolog("student_data(StudentID, Name, Email, School, Programme)")

            if not students:
                ctk.CTkLabel(self, text="No students found.", text_color="red").pack(pady=10)
                return

            for student in students:
                student_id = student["StudentID"]
                name = student["Name"]
                email = student["Email"]
                school = student["School"]
                programme = student["Programme"]

                # Calculate cumulative GPA dynamically
                cumulative_gpa = self.get_cumulative_gpa(student_id, "2023/2024")

                # Check if the student is on academic probation
                if cumulative_gpa <= 2.0:  # Adjust the threshold as needed
                    self.send_email_alert(student_id, name, email, programme, school)
                    print(f"Alert sent for {name} (ID: {student_id})")

            ctk.CTkLabel(self, text="Alerts sent successfully!", text_color="green").pack(pady=10)
        except Exception as e:
            print(f"Error sending alerts: {e}")
            ctk.CTkLabel(self, text="Error sending alerts.", text_color="red").pack(pady=10)

    def show_add_student_screen(self):
        """Display the screen to add a new student."""
        for widget in self.winfo_children():
            widget.destroy()

        title_label = ctk.CTkLabel(self, text="Add New Student", font=("Arial", 24))
        title_label.pack(pady=20)

        # Input fields for student details
        student_id_label = ctk.CTkLabel(self, text="Student ID:")
        student_id_label.pack(pady=5)
        student_id_entry = ctk.CTkEntry(self)
        student_id_entry.pack(pady=5)

        name_label = ctk.CTkLabel(self, text="Name:")
        name_label.pack(pady=5)
        name_entry = ctk.CTkEntry(self)
        name_entry.pack(pady=5)

        email_label = ctk.CTkLabel(self, text="Email:")
        email_label.pack(pady=5)
        email_entry = ctk.CTkEntry(self)
        email_entry.pack(pady=5)

        school_label = ctk.CTkLabel(self, text="School:")
        school_label.pack(pady=5)
        school_entry = ctk.CTkEntry(self)
        school_entry.pack(pady=5)

        programme_label = ctk.CTkLabel(self, text="Programme:")
        programme_label.pack(pady=5)
        programme_entry = ctk.CTkEntry(self)
        programme_entry.pack(pady=5)

        # Submit button
        submit_button = ctk.CTkButton(
            self, text="Add Student",
            command=lambda: self.add_student_to_db(
                student_id_entry.get(),
                name_entry.get(),
                email_entry.get(),
                school_entry.get(),
                programme_entry.get()
            )
        )
        submit_button.pack(pady=20)

        # Back button
        back_button = ctk.CTkButton(self, text="Back", command=self.show_admin_dashboard)
        back_button.pack(pady=10)

        
    def add_student_to_db(self, student_id, name, email, school, programme):
        """Add a new student to the database."""
        try:
            # Validate input
            if not (student_id and name and email and school and programme):
                ctk.CTkLabel(self, text="All fields are required.", text_color="red").pack(pady=10)
                return

            # Insert the student into the database
            query = """
            INSERT INTO students (student_id, name, email, school, programme)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (student_id, name, email, school, programme))
            db.commit()
            ctk.CTkLabel(self, text="Student added successfully!", text_color="green").pack(pady=10)

            # Return to admin dashboard
            self.show_admin_dashboard()
        except Exception as e:
            print(f"Error adding student: {e}")
            ctk.CTkLabel(self, text="Error adding student. Please try again.", text_color="red").pack(pady=10)
            

        
    def show_student_dashboard(self, student_id):
        """Display the Student Dashboard."""
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        # Add title
        title_label = ctk.CTkLabel(self, text="Student Dashboard", font=("Arial", 24))
        title_label.pack(pady=20)

        # Add button to view GPA report
        view_gpa_button = ctk.CTkButton(
            self, text="View GPA Report",
            command=lambda: self.display_student_gpa_report(student_id)
        )
        view_gpa_button.pack(pady=10)

        # Add button to check academic probation status
        probation_status_button = ctk.CTkButton(
            self, text="Check Academic Probation",
            command=lambda: self.check_student_probation(student_id)
        )
        probation_status_button.pack(pady=10)

        # Add log out button
        back_button = ctk.CTkButton(self, text="Log Out", command=self.show_home_screen)
        back_button.pack(pady=20)


    def display_student_gpa_report(self, student_id):
        """Display the GPA report for the student."""
        self.populate_prolog_from_db()  # Ensure Prolog facts are updated

        gpa1 = self.get_student_gpa(student_id, 1)
        gpa2 = self.get_student_gpa(student_id, 2)
        cumulative_gpa = self.get_cumulative_gpa(student_id, "2023/2024")

        report = (
            f"Student ID: {student_id}\n"
            f"GPA Semester 1: {gpa1}\n"
            f"GPA Semester 2: {gpa2}\n"
            f"Cumulative GPA: {cumulative_gpa}"
        )
        # Display the report
        ctk.CTkLabel(self, text=report, text_color="black", wraplength=500).pack(pady=20)


    def check_student_probation(self, student_id):
        """Check if the student is on academic probation."""
        self.populate_prolog_from_db()  # Ensure the Prolog facts are up-to-date

        if self.is_on_academic_probation(student_id):
            ctk.CTkLabel(self, text="You are on academic probation!", text_color="red").pack(pady=20)
        else:
            ctk.CTkLabel(self, text="You are not on academic probation.", text_color="green").pack(pady=20)


    

# Run the application
if __name__ == "__main__":
    from testpython import get_student_gpa, get_cumulative_gpa, is_on_academic_probation, populate_prolog_from_db, query_prolog, send_email_alert

    app = AcademicProbationApp(
        get_student_gpa=get_student_gpa,
        get_cumulative_gpa=get_cumulative_gpa,
        is_on_academic_probation=is_on_academic_probation,
        populate_prolog_from_db=populate_prolog_from_db,
        query_prolog=query_prolog,
        send_email_alert=send_email_alert
 )
    app.mainloop()
