import customtkinter as ctk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import time

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

        # Load the logo image
        self.logo_image = Image.open("logo.png")  # Change to your image path
        self.logo_image = self.logo_image.resize((300, 300), Image.Resampling.LANCZOS)  # Resize if necessary
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)

        # Window settings
        self.title("Academic Probation System")
        self.geometry("1200x800")

        # Start with the home screen
        self.show_home_screen()

    def create_user_for_new_student(self, student_id, email):
        """Create a user for the new student."""
        try:
            # Hash the student ID for password
            import bcrypt
            hashed_password = bcrypt.hashpw(str(student_id).encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            # Insert user into the database
            query = """
            INSERT INTO users (username, password_hash, role, student_id)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (email, hashed_password, 'student', student_id))
            db.commit()
            print(f"User created successfully for student {student_id}.")
        except Exception as e:
            print(f"Error creating user for student {student_id}: {e}")    

    def show_home_screen(self):
        """Display the home screen with Student and Admin login options."""
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        # Add logo image at the top-left corner
        logo_label = ctk.CTkLabel(self, image=self.logo_photo, text=None)
        logo_label.place(x=520, y=10)     

        # Add title
        title_label = ctk.CTkLabel(self, text="Academic Probation System", font=("Arial", 24))
        title_label.pack(pady=(250, 50))

        # Add buttons for Student and Admin login
        student_button = ctk.CTkButton(self, text="Student Login", command=self.show_student_login)
        student_button.pack(pady=20)

        admin_button = ctk.CTkButton(self, text="Admin Login", command=self.show_admin_login)
        admin_button.pack(pady=20)

        title_label = ctk.CTkLabel(self, text="by ScholarSync", font=("Arial", 24))
        title_label.pack(pady=10)

        subtext_label = ctk.CTkLabel(self, text="Daryn Brown, Briana Taylor, Justin Alder, Marvis Haughton", font=("Arial", 16))  # Smaller font for subtext
        subtext_label.pack(pady=(0, 50))  # No padding above, 50px padding below

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
        username_entry = ctk.CTkEntry(self, width=300)
        username_entry.pack(pady=10)

        password_label = ctk.CTkLabel(self, text="Password:")
        password_label.pack(pady=10)
        password_entry = ctk.CTkEntry(self, show="*", width=300)
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
        username_entry = ctk.CTkEntry(self, width=300)
        username_entry.pack(pady=10)

        password_label = ctk.CTkLabel(self, text="Password:")
        password_label.pack(pady=10)
        password_entry = ctk.CTkEntry(self, show="*", width=300)
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

        # Add button to add a new module
        add_module_button = ctk.CTkButton(
            self, text="Add New Module",
            command=self.show_add_module_screen
        )
        add_module_button.pack(pady=10)

        # Button to manage module details
        module_details_button = ctk.CTkButton(
            self, text="Module Details",
            command=self.show_module_details_screen
        )
        module_details_button.pack(pady=10)

        # Log out button
        back_button = ctk.CTkButton(self, text="Log Out", command=self.show_home_screen)
        back_button.pack(pady=20)

    def show_add_module_screen(self):
        """Screen to add a new module."""
        for widget in self.winfo_children():
            widget.destroy()

        title_label = ctk.CTkLabel(self, text="Add New Module", font=("Arial", 24))
        title_label.pack(pady=20)

        # Input fields for module details
        module_id_label = ctk.CTkLabel(self, text="Module ID:")
        module_id_label.pack(pady=5)
        module_id_entry = ctk.CTkEntry(self, width=300)
        module_id_entry.pack(pady=5)

        module_name_label = ctk.CTkLabel(self, text="Module Name:")
        module_name_label.pack(pady=5)
        module_name_entry = ctk.CTkEntry(self, width=300)
        module_name_entry.pack(pady=5)

        credits_label = ctk.CTkLabel(self, text="Credits:")
        credits_label.pack(pady=5)
        credits_entry = ctk.CTkEntry(self, width=300)
        credits_entry.pack(pady=5)

        # Submit button
        submit_button = ctk.CTkButton(
            self, text="Add Module",
            command=lambda: self.add_module_to_db(
                module_id_entry.get(),
                module_name_entry.get(),
                credits_entry.get()
            )
        )
        submit_button.pack(pady=20)

        # Back button
        back_button = ctk.CTkButton(self, text="Back", command=self.show_admin_dashboard)
        back_button.pack(pady=10)
        

    def add_module_to_db(self, module_id, module_name, credits):
        """Add a new module to the database."""
        try:
            # Validate input
            if not (module_id and module_name and credits.isdigit()):
                ctk.CTkLabel(self, text="All fields are required and credits must be a number.", text_color="red").pack(pady=10)
                return

            # Insert the module into the database
            query = """
            INSERT INTO modules (module_id, module_name, credits)
            VALUES (%s, %s, %s)
            """
            cursor.execute(query, (module_id, module_name, int(credits)))
            db.commit()

            ctk.CTkLabel(self, text="Module added successfully!", text_color="green").pack(pady=10)

            # Return to admin dashboard
            self.show_admin_dashboard()
        except Exception as e:
            print(f"Error adding module: {e}")
            ctk.CTkLabel(self, text="Error adding module. Please try again.", text_color="red").pack(pady=10)
        


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
        """Submit the new default GPA to Prolog and update probation statuses."""
        try:
            # Update the default GPA in Prolog
            self.query_prolog(f"update_default_gpa({float(gpa)})")
            
            # Clear the screen and display success message
            ctk.CTkLabel(self, text="Default GPA updated successfully!", text_color="green").pack(pady=20)

            # Optionally, display updated probation statuses
            self.show_updated_probation_statuses()
        except Exception as e:
            print(f"Error: {e}")
            ctk.CTkLabel(self, text="Error updating default GPA.", text_color="red").pack(pady=20)

    def show_updated_probation_statuses(self):
        """Display updated probation statuses for all students."""
        try:
            students = self.query_prolog("student_data(StudentID, Name, _, _, _)")
            if not students:
                raise Exception("No students found in the database.")
            
            # Clear the screen
            for widget in self.winfo_children():
                widget.destroy()
            
            # Add title
            title_label = ctk.CTkLabel(self, text="Updated Probation Statuses", font=("Arial", 24))
            title_label.pack(pady=20)
            
            # Display statuses in a table
            table_frame = ctk.CTkFrame(self)
            table_frame.pack(pady=10, padx=10, fill="both", expand=True)

            columns = ("Student ID", "Name", "Probation Status")
            status_table = ttk.Treeview(table_frame, columns=columns, show="headings")

            # Set up column headings
            for col in columns:
                status_table.heading(col, text=col)
                status_table.column(col, anchor="center", width=200)

            # Add probation status for each student
            for student in students:
                student_id = student["StudentID"]
                name = student["Name"]
                probation_status = "Yes" if self.query_prolog(f"on_academic_probation({student_id})") else "No"
                status_table.insert("", "end", values=(student_id, name, probation_status))

            status_table.pack(fill="both", expand=True)

            # Back button
            back_button = ctk.CTkButton(self, text="Back", command=self.show_admin_dashboard)
            back_button.pack(pady=20)
        except Exception as e:
            print(f"Error displaying probation statuses: {e}")
            ctk.CTkLabel(self, text="Error displaying updated statuses.", text_color="red").pack(pady=20)

    def record_gpa(self):
        """Screen to record/update GPA."""
        for widget in self.winfo_children():
            widget.destroy()

        title_label = ctk.CTkLabel(self, text="Record or Update GPA", font=("Arial", 24))
        title_label.pack(pady=20)

        student_id_label = ctk.CTkLabel(self, text="Student ID:")
        student_id_label.pack(pady=10)
        student_id_entry = ctk.CTkEntry(self, width=300)
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
        student_id_entry = ctk.CTkEntry(self, width=300)
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
                # Fetch GPA values
                gpa1 = self.get_student_gpa(student_id, 1)
                gpa2 = self.get_student_gpa(student_id, 2)
                cumulative_gpa = self.get_cumulative_gpa(student_id, "2023/2024")

                # Format GPA values to two decimal places
                gpa1_formatted = f"{gpa1:.2f}"
                gpa2_formatted = f"{gpa2:.2f}"
                cumulative_gpa_formatted = f"{cumulative_gpa:.2f}"

                # Clear existing widgets
                for widget in self.winfo_children():
                    widget.destroy()

                # Create the styled report text
                report = (
                    f"Student ID: {result[0]}\n"
                    f"Name: {result[1]}\n"
                    f"Email: {result[2]}\n"
                    f"School: {result[3]}\n"
                    f"Programme: {result[4]}\n"
                    f"GPA Semester 1: {gpa1_formatted}\n"
                    f"GPA Semester 2: {gpa2_formatted}\n"
                    f"Cumulative GPA: {cumulative_gpa_formatted}"
                )

                # Display the report with larger text and white color
                ctk.CTkLabel(
                    self,
                    text=report,
                    text_color="white",  # Set text color to white
                    font=("Arial", 32),  # Double the default font size
                    wraplength=800  # Ensure text wraps nicely within the window
                ).pack(pady=20)

                # Add a back button to return to the Generate Report screen
                back_button = ctk.CTkButton(self, text="Back", command=self.generate_report)
                back_button.pack(pady=20)
            else:
                # Display error message if student is not found
                ctk.CTkLabel(self, text="Student not found.", text_color="red", font=("Arial", 24)).pack(pady=10)

                # Back button to return to Generate Report screen
                back_button = ctk.CTkButton(self, text="Back", command=self.generate_report)
                back_button.pack(pady=20)
        except Exception as e:
            print(f"Error: {e}")
            ctk.CTkLabel(self, text="Error generating report.", text_color="red", font=("Arial", 24)).pack(pady=10)

            # Back button to return to Generate Report screen
            back_button = ctk.CTkButton(self, text="Back", command=self.generate_report)
            back_button.pack(pady=20)

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
        student_id_entry = ctk.CTkEntry(self, width=300)
        student_id_entry.pack(pady=5)

        name_label = ctk.CTkLabel(self, text="Name:")
        name_label.pack(pady=5)
        name_entry = ctk.CTkEntry(self, width=300)
        name_entry.pack(pady=5)

        email_label = ctk.CTkLabel(self, text="Email:")
        email_label.pack(pady=5)
        email_entry = ctk.CTkEntry(self, width=300)
        email_entry.pack(pady=5)

        school_label = ctk.CTkLabel(self, text="School:")
        school_label.pack(pady=5)
        school_entry = ctk.CTkEntry(self, width=300)
        school_entry.pack(pady=5)

        programme_label = ctk.CTkLabel(self, text="Programme:")
        programme_label.pack(pady=5)
        programme_entry = ctk.CTkEntry(self, width=300)
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

            # Create user for the student
            self.create_user_for_new_student(student_id, email)

            # Return to admin dashboard
            self.show_admin_dashboard()
        except Exception as e:
            print(f"Error adding student: {e}")
            ctk.CTkLabel(self, text="Error adding student. Please try again.", text_color="red").pack(pady=10)
            
    from db_connection import cursor, db

    
        
        
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
        self.populate_prolog_from_db(student_id=student_id)  # Ensure Prolog facts are updated

        # Fetch GPA values
        gpa1 = self.get_student_gpa(student_id, 1)
        gpa2 = self.get_student_gpa(student_id, 2)
        cumulative_gpa = self.get_cumulative_gpa(student_id, "2023/2024")

        # Format GPA values to two decimal places
        gpa1_formatted = f"{gpa1:.2f}"
        gpa2_formatted = f"{gpa2:.2f}"
        cumulative_gpa_formatted = f"{cumulative_gpa:.2f}"

        # Create the report text
        report = (
            f"Student ID: {student_id}\n"
            f"GPA Semester 1: {gpa1_formatted}\n"
            f"GPA Semester 2: {gpa2_formatted}\n"
            f"Cumulative GPA: {cumulative_gpa_formatted}"
        )

        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        # Display the report with larger text and white color
        ctk.CTkLabel(
            self, 
            text=report, 
            text_color="white",  # Set text color to white
            font=("Arial", 32),  # Double the default font size
            wraplength=800  # Ensure text wraps nicely within the window
        ).pack(pady=20)

        # Add a back button that passes the `student_id`
        back_button = ctk.CTkButton(self, text="Back", command=lambda: self.show_student_dashboard(student_id))
        back_button.pack(pady=20)


    def check_student_probation(self, student_id):
        """Check if the student is on academic probation."""
        self.populate_prolog_from_db()  # Ensure the Prolog facts are up-to-date

        if self.is_on_academic_probation(student_id):
            ctk.CTkLabel(self, text="You are on academic probation!", text_color="red").pack(pady=20)
        else:
            ctk.CTkLabel(self, text="You are not on academic probation.", text_color="green").pack(pady=20)

    def get_module_ids(self):
        """Fetch existing module IDs from the database."""
        try:
            query = "SELECT module_id FROM modules"
            cursor.execute(query)
            return [str(row[0]) for row in cursor.fetchall()]  # Convert to strings
        except Exception as e:
            print(f"Error fetching module IDs: {e}")
            return []

    def get_student_ids(self):
        """Fetch existing student IDs from the database."""
        try:
            query = "SELECT student_id FROM students"
            cursor.execute(query)
            return [str(row[0]) for row in cursor.fetchall()]  # Convert to strings
        except Exception as e:
            print(f"Error fetching student IDs: {e}")
            return []

            

    def show_module_details_screen(self):
        """Display the screen to manage module details."""
        for widget in self.winfo_children():
            widget.destroy()

        title_label = ctk.CTkLabel(self, text="Module Details", font=("Arial", 24))
        title_label.pack(pady=20)

        # Fetch data for dropdowns
        module_ids = self.get_module_ids()
        student_ids = self.get_student_ids()
        letter_grades = ["A+", "A", "B+", "B", "C+", "C", "D+", "D", "F"]

        # Module ID dropdown
        module_id_label = ctk.CTkLabel(self, text="Module ID:")
        module_id_label.pack(pady=5)
        module_id_dropdown = ctk.CTkComboBox(self, values=module_ids, width=300)  # Now module_ids are strings
        module_id_dropdown.pack(pady=5)

        # Student ID dropdown
        student_id_label = ctk.CTkLabel(self, text="Student ID:")
        student_id_label.pack(pady=5)
        student_id_dropdown = ctk.CTkComboBox(self, values=student_ids, width=300)  # Now student_ids are strings
        student_id_dropdown.pack(pady=5)

        # Letter Grade dropdown
        letter_grade_label = ctk.CTkLabel(self, text="Letter Grade:")
        letter_grade_label.pack(pady=5)
        letter_grade_dropdown = ctk.CTkComboBox(self, values=letter_grades, width=300)
        letter_grade_dropdown.pack(pady=5)


        # Input fields for module details
        # module_id_label = ctk.CTkLabel(self, text="Module ID:")
        # module_id_label.pack(pady=5)
        # module_id_entry = ctk.CTkEntry(self, width=300)
        # module_id_entry.pack(pady=5)

        # Module Name (Editable field)
        module_name_label = ctk.CTkLabel(self, text="Module Name:")
        module_name_label.pack(pady=5)
        module_name_entry = ctk.CTkEntry(self, width=300)
        module_name_entry.pack(pady=5)

        # Fetch module name dynamically
        def fetch_module_name(module_id):
            try:
                query = "SELECT module_name FROM modules WHERE module_id = %s"
                cursor.execute(query, (module_id,))
                result = cursor.fetchone()
                return result[0] if result else ""
            except Exception as e:
                print(f"Error fetching module name: {e}")
                return "Error"

        # Update module name field in real-time
        def update_module_name():
            last_selected_id = None
            while True:
                selected_module_id = module_id_dropdown.get()
                if selected_module_id != last_selected_id:
                    last_selected_id = selected_module_id
                    module_name = fetch_module_name(selected_module_id)
                    if module_name_entry.get() != module_name:
                        module_name_entry.delete(0, "end")
                        module_name_entry.insert(0, module_name)
                time.sleep(0.1)

        # Start thread to monitor module ID selection
        threading.Thread(target=update_module_name, daemon=True).start()


        year_label = ctk.CTkLabel(self, text="Year:")
        year_label.pack(pady=5)
        year_entry = ctk.CTkEntry(self, width=300)
        year_entry.pack(pady=5)

        semester_label = ctk.CTkLabel(self, text="Semester:")
        semester_label.pack(pady=5)
        semester_entry = ctk.CTkEntry(self, width=300)
        semester_entry.pack(pady=5)

        # Grade Points (Editable field)
        grade_points_label = ctk.CTkLabel(self, text="Grade Points:")
        grade_points_label.pack(pady=5)
        grade_points_entry = ctk.CTkEntry(self, width=300)
        grade_points_entry.pack(pady=5)

        # Mapping from letter grades to grade points
        grade_to_points = {
            "A+": 4.3, "A": 4.0, "A-": 3.7,
            "B+": 3.3, "B": 3.0, "B-": 2.7,
            "C+": 2.3, "C": 2.0, "C-": 1.7,
            "D+": 1.3, "D": 1.0, "F": 0.0
        }

        # Function to update grade points in real time
        def update_grade_points():
            while True:
                selected_grade = letter_grade_dropdown.get()
                if selected_grade in grade_to_points:
                    current_points = grade_to_points[selected_grade]
                    if grade_points_entry.get() != str(current_points):
                        grade_points_entry.delete(0, "end")
                        grade_points_entry.insert(0, str(current_points))
                time.sleep(0.1)  # Small delay to reduce CPU usage

        # Start a thread to monitor and update grade points
        threading.Thread(target=update_grade_points, daemon=True).start()

        # Buttons for Save, Update, and Delete
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        save_button = ctk.CTkButton(
            button_frame,
            text="Save",
            command=lambda: self.save_module_details(
                module_id_dropdown.get(),
                year_entry.get(),
                semester_entry.get(),
                student_id_dropdown.get(),
                letter_grade_dropdown.get()
            ),
        )
        save_button.grid(row=0, column=0, padx=10)



        delete_button = ctk.CTkButton(
            button_frame, text="Delete",
            command=lambda: self.delete_module_details(module_id_dropdown.get())
        )
        delete_button.grid(row=0, column=2, padx=10)

        # Back button
        back_button = ctk.CTkButton(self, text="Back", command=self.show_admin_dashboard)
        back_button.pack(pady=10)

    def update_module_name(self, module_id, module_name_field):
        """Fetch and update the module name based on the selected Module ID."""
        try:
            query = "SELECT module_name FROM modules WHERE module_id = %s"
            cursor.execute(query, (module_id,))
            result = cursor.fetchone()

            if result:
                module_name_field.configure(text=result[0])  # Update the Module Name field
                module_name_field.configure(fg_color="gray", text_color="blue")  # White background with blue text
            else:
                module_name_field.configure(text="Not Found", fg_color="red", text_color="white")  # Error case
        except Exception as e:
            print(f"Error fetching module name: {e}")
            module_name_field.configure(text="Error", fg_color="red", text_color="white")
    
    def save_module_details(self, module_id, year, semester, student_id, letter_grade):
        """Save new module details to the database."""
        try:
            query = """
            INSERT INTO module_details (module_id, academic_year, semester, student_id, letter_grade)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (module_id, year, semester, student_id, letter_grade))
            db.commit()

            self.populate_prolog_from_db(student_id=student_id, academic_year=year, semester=semester)
            self.query_prolog(f"recalculate_semester_gpa({student_id}, '{year}', {semester})")
            self.query_prolog(f"recalculate_cumulative_gpa({student_id}, '{year}')")

            
            ctk.CTkLabel(self, text="Module Details successfully added!", text_color="green").pack(pady=10)
        except Exception as e:
            print(f"Error adding module details: {e}")
            ctk.CTkLabel(self, text="Error adding module details. Please try again.", text_color="red").pack(pady=10)

            
    def update_module_details(self, module_id, year, semester, student_id, letter_grade):
        """Update existing module details in the database."""
        try:
            query = """
            UPDATE module_details
            SET academic_year = %s, semester = %s, letter_grade = %s
            WHERE module_id = %s AND student_id = %s
            """
            cursor.execute(query, (year, semester, letter_grade, module_id, student_id))
            db.commit()

            self.populate_prolog_from_db(student_id=student_id, academic_year=year, semester=semester)
            self.query_prolog(f"recalculate_semester_gpa({student_id}, '{year}', {semester})")
            self.query_prolog(f"recalculate_cumulative_gpa({student_id}, '{year}')")

            
            ctk.CTkLabel(self, text="Module Details successfully updated!", text_color="green").pack(pady=10)
        except Exception as e:
            print(f"Error updating module details: {e}")
            ctk.CTkLabel(self, text="Error updating module details. Please try again.", text_color="red").pack(pady=10)


    def delete_module_details(self, module_id, student_id):
        """Delete module details from the database."""
        try:
            query = "DELETE FROM module_details WHERE module_id = %s AND student_id = %s"
            cursor.execute(query, (module_id, student_id))
            db.commit()
            ctk.CTkLabel(self, text="Module Details successfully deleted!", text_color="green").pack(pady=10)
        except Exception as e:
            print(f"Error deleting module details: {e}")
            ctk.CTkLabel(self, text="Error deleting module details. Please try again.", text_color="red").pack(pady=10)

    

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
