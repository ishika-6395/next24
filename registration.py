from tkinter import *
from tkinter import messagebox, ttk, filedialog
import random
import re
import sqlite3
from datetime import datetime
from PIL import Image, ImageTk
import bcrypt

class RegistrationForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Registration System")
        self.root.geometry("800x900")
        self.root.configure(bg="#F5F5DC")  # Beige background
        self.reg_number = self.generate_registration_number()
        # Create scrollable canvas
        self.canvas = Canvas(root, bg="#F5F5DC")
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas, bg="#F5F5DC")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack scrollbar and canvas
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Initialize variables
        self.profile_image = None
        self.terms_var = BooleanVar()
        self.password_visible = False
        self.gender_var = StringVar()
        
        # Configure style
        style = ttk.Style()
        style.configure("Custom.TEntry", 
                       fieldbackground="white",
                       foreground="black")
        
        style.configure("Custom.TButton",
                       padding=10,
                       font=("Helvetica", 12))
        
        self.create_widgets()
        self.create_database()
    def generate_registration_number(self):
        current_year = datetime.now().year
        random_num = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        return f"REG{current_year}{random_num}"
    def create_widgets(self):
        # Title
        title_frame = Frame(self.scrollable_frame, bg="#F5F5DC", pady=20)
        title_frame.pack(fill=X)
        
        Label(title_frame, 
              text="Advanced Registration System",
              font=("Montserrat", 28, "bold"),
              bg="#F5F5DC",
              fg="black").pack()

        # Main content frame
        content_frame = Frame(self.scrollable_frame, bg="#F5F5DC", pady=10)
        content_frame.pack(fill=X, padx=20)

        # Left frame for form fields
        form_frame = Frame(content_frame, bg="#F5F5DC")
        form_frame.pack(side=LEFT, fill=X, expand=True)

        # Right frame for profile picture
        profile_frame = Frame(content_frame, bg="#F5F5DC", padx=20)
        profile_frame.pack(side=RIGHT, fill=Y)
        
        self.profile_label = Label(profile_frame, 
                                 text="Click to add\nprofile picture",
                                 width=15,
                                 height=7,
                                 bg="white",
                                 fg="black")
        self.profile_label.pack(pady=10)
        self.profile_label.bind("<Button-1>", self.upload_profile_picture)

        # Form fields
        fields_frame = Frame(form_frame, bg="#F5F5DC", pady=20)
        fields_frame.pack(fill=X)

        # Create fields
        self.create_entry_field(fields_frame, "👤 Full Name:", "name")
        self.create_entry_field(fields_frame, "📧 Email:", "email")
        self.create_password_field(fields_frame)
        self.create_entry_field(fields_frame, "🎂 Age:", "age")
        self.create_entry_field(fields_frame, "📱 Phone:", "phone")
        self.create_address_field(fields_frame)
        self.create_gender_field(fields_frame)
        self.create_entry_field(fields_frame, "📚 Education:", "education")
        
        reg_frame = Frame(fields_frame, bg="#F5F5DC", pady=5)
        reg_frame.pack(fill=X)
        Label(reg_frame,text="🔢 Reg. Number:",
              font=("Helvetica", 12),
              bg="#F5F5DC",
              fg="black",
              width=15,
              anchor="w").pack(side=LEFT)
        
        self.reg_entry = ttk.Entry(reg_frame,
                                 font=("Helvetica", 12),
                                 style="Custom.TEntry",
                                 state='readonly')
        self.reg_entry.pack(side=LEFT, fill=X, expand=True)
        self.reg_entry.insert(0, self.reg_number)

        # Terms and conditions
        terms_frame = Frame(self.scrollable_frame, bg="#F5F5DC", pady=10)
        terms_frame.pack(fill=X, padx=50)
        
        Checkbutton(terms_frame,
                    text="I agree to the Terms and Conditions",
                    variable=self.terms_var,
                    bg="#F5F5DC",
                    fg="black",
                    selectcolor="white",
                    activebackground="#F5F5DC").pack()

        # Buttons
        button_frame = Frame(self.scrollable_frame, bg="#F5F5DC", pady=20)
        button_frame.pack(fill=X, padx=50)

        self.submit_btn = ttk.Button(button_frame,
                                   text="Register",
                                   style="Custom.TButton",
                                   command=self.save_details)
        self.submit_btn.pack(side=LEFT, padx=5, expand=True)

        self.clear_btn = ttk.Button(button_frame,
                                  text="Clear Form",
                                  style="Custom.TButton",
                                  command=self.clear_form)
        self.clear_btn.pack(side=LEFT, padx=5, expand=True)

    def create_entry_field(self, parent, label_text, attr_name):
        frame = Frame(parent, bg="#F5F5DC", pady=5)
        frame.pack(fill=X)
        
        Label(frame,
              text=label_text,
              font=("Helvetica", 12),
              bg="#F5F5DC",
              fg="black",
              width=15,
              anchor="w").pack(side=LEFT)
        
        entry = ttk.Entry(frame, 
                         font=("Helvetica", 12),
                         style="Custom.TEntry")
        entry.pack(side=LEFT, fill=X, expand=True)
        
        setattr(self, f"{attr_name}_entry", entry)

    def create_password_field(self, parent):
        frame = Frame(parent, bg="#F5F5DC", pady=5)
        frame.pack(fill=X)
        
        Label(frame,
              text="🔒 Password:",
              font=("Helvetica", 12),
              bg="#F5F5DC",
              fg="black",
              width=15,
              anchor="w").pack(side=LEFT)
        
        password_frame = Frame(frame, bg="#F5F5DC")
        password_frame.pack(side=LEFT, fill=X, expand=True)
        
        self.password_entry = ttk.Entry(password_frame,
                                      font=("Helvetica", 12),
                                      show="*",
                                      style="Custom.TEntry")
        self.password_entry.pack(side=LEFT, fill=X, expand=True)
        
        self.toggle_btn = ttk.Button(password_frame,
                                   text="👁",
                                   width=3,
                                   style="Custom.TButton",
                                   command=self.toggle_password)
        self.toggle_btn.pack(side=LEFT)

        self.strength_var = StringVar(value="Weak")
        self.strength_label = Label(frame,
                                  textvariable=self.strength_var,
                                  bg="#F5F5DC",
                                  fg="red",
                                  width=10)
        self.strength_label.pack(side=LEFT)
        
        self.password_entry.bind("<KeyRelease>", self.check_password_strength)

    def create_address_field(self, parent):
        frame = Frame(parent, bg="#F5F5DC", pady=5)
        frame.pack(fill=X)
        
        Label(frame,
              text="📍 Address:",
              font=("Helvetica", 12),
              bg="#F5F5DC",
              fg="black",
              width=15,
              anchor="w").pack(side=LEFT)
        
        self.address_entry = Text(frame,
                                font=("Helvetica", 12),
                                height=3,
                                bg="white",
                                fg="black")
        self.address_entry.pack(side=LEFT, fill=X, expand=True)

    def create_gender_field(self, parent):
        frame = Frame(parent, bg="#F5F5DC", pady=5)
        frame.pack(fill=X)
        
        Label(frame,
              text="⚧ Gender:",
              font=("Helvetica", 12),
              bg="#F5F5DC",
              fg="black",
              width=15,
              anchor="w").pack(side=LEFT)
        
        gender_frame = Frame(frame, bg="#F5F5DC")
        gender_frame.pack(side=LEFT, fill=X)
        
        # Set a default value for gender_var
        self.gender_var.set(None)  # Add this line
        
        genders = [("Male", "male"), ("Female", "female"), 
                  ("Other", "other"), ("Prefer not to say", "prefer_not_to_say")]
        
        for text, value in genders:
            Radiobutton(gender_frame,
                       text=text,
                       variable=self.gender_var,
                       value=value,
                       bg="#F5F5DC",
                       fg="black",
                       selectcolor="white",
                       activebackground="#F5F5DC",
                       indicatoron=True).pack(side=LEFT, padx=10)
    def upload_profile_picture(self, event=None):
        file_types = [('Image Files', '*.jpg *.png *.gif *.bmp')]
        file_path = filedialog.askopenfilename(filetypes=file_types)
        
        if file_path:
            try:
                image = Image.open(file_path)
                image = image.resize((100, 100), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                
                self.profile_label.config(image=photo, text="")
                self.profile_label.image = photo
                self.profile_image = file_path
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    def toggle_password(self):
        self.password_visible = not self.password_visible
        self.password_entry.config(show="" if self.password_visible else "*")
        self.toggle_btn.config(text="👁" if self.password_visible else "👁️‍🗨️")

    def check_password_strength(self, event=None):
        password = self.password_entry.get()
        strength = 0
        
        if len(password) >= 8: strength += 1
        if re.search(r"[A-Z]", password): strength += 1
        if re.search(r"[a-z]", password): strength += 1
        if re.search(r"[0-9]", password): strength += 1
        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): strength += 1
        
        if strength == 0:
            self.strength_var.set("Very Weak")
            self.strength_label.config(fg="red")
        elif strength <= 2:
            self.strength_var.set("Weak")
            self.strength_label.config(fg="orange")
        elif strength <= 3:
            self.strength_var.set("Medium")
            self.strength_label.config(fg="yellow")
        elif strength <= 4:
            self.strength_var.set("Strong")
            self.strength_label.config(fg="light green")
        else:
            self.strength_var.set("Very Strong")
            self.strength_label.config(fg="green")

    def create_database(self):
        conn = sqlite3.connect('registration.db')
        cursor = conn.cursor()
        
        cursor.execute('DROP TABLE IF EXISTS users')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                age INTEGER,
                phone TEXT,
                education TEXT,
                registration_number TEXT UNIQUE,
                address TEXT,
                gender TEXT,
                profile_image TEXT,
                registration_date DATETIME
            )
        ''')
        conn.commit()
        conn.close()

    def validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def validate_phone(self, phone):
        pattern = r'^\+?1?\d{9,15}$'
        return re.match(pattern, phone) is not None

    def save_details(self):
        if not self.terms_var.get():
            messagebox.showwarning("Terms & Conditions", "Please accept the terms and conditions")
            return

        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        age = self.age_entry.get().strip()
        phone = self.phone_entry.get().strip()
        address = self.address_entry.get("1.0", END).strip()
        gender = self.gender_var.get()

        if not all([name, email, password, age, phone, address, gender]):
            messagebox.showwarning("Validation Error", "All fields are required!")
            return

        if not self.validate_email(email):
            messagebox.showerror("Validation Error", "Invalid email format!")
            return

        if not self.validate_phone(phone):
            messagebox.showerror("Validation Error", "Invalid phone number!")
            return
        education = self.education_entry.get().strip()

        if not all([name, email, password, age, phone, education, address, gender]):
            messagebox.showwarning("Validation Error", "All fields are required!")
            return   

        try:
            age = int(age)
            if age <= 0 or age > 120:
                raise ValueError
        except ValueError:
            messagebox.showerror("Validation Error", "Invalid age!")
            return

        if self.strength_var.get() in ["Very Weak", "Weak"]:
            if not messagebox.askyesno("Weak Password", "Your password is weak. Do you want to continue?"):
                return

        try:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            conn = sqlite3.connect('registration.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (name, email, password, age, phone, education,
                                 registration_number, address, gender, 
                                 profile_image, registration_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, email, hashed_password, age, phone, education,
                  self.reg_number, address, gender,
                  self.profile_image, datetime.now()))
            
            conn.commit()
            reg_window = Toplevel(self.root)
            reg_window.title("Registration Successful")
            reg_window.geometry("500x300")
            reg_window.configure(bg="#F0F8FF")  # Light blue background
            
            # Center the window
            window_width = 500
            window_height = 300
            screen_width = reg_window.winfo_screenwidth()
            screen_height = reg_window.winfo_screenheight()
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            reg_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
            
            # Success icon and messages
            success_frame = Frame(reg_window, bg="#F0F8FF", pady=20)
            success_frame.pack(fill=X)
            
            Label(success_frame,
                text="✅ Registration Successful!",
                font=("Montserrat", 20, "bold"),
                bg="#F0F8FF",
                fg="#228B22").pack(pady=10)  # Forest green color
                
            Label(reg_window,
                text="Your Registration Number is:",
                font=("Helvetica", 14),
                bg="#F0F8FF",
                fg="#333333").pack()
                
            reg_num_frame = Frame(reg_window, bg="#E8F4FF", padx=20, pady=10)
            reg_num_frame.pack(pady=15)
            
            Label(reg_num_frame,
                text=self.reg_number,
                font=("Consolas", 24, "bold"),
                bg="#E8F4FF",
                fg="#0066cc").pack()
                
            ttk.Button(reg_window,
                    text="OK",
                    style="Custom.TButton",
                    command=reg_window.destroy).pack(pady=20)
            
            # Make window modal
            reg_window.transient(self.root)
            reg_window.grab_set()
            
            self.clear_form()
                
        except sqlite3.IntegrityError as e:
            if "registration_number" in str(e):
                self.reg_number = self.generate_registration_number()
                self.save_details()  # Retry with new registration number
            else:
                messagebox.showerror("Error", "Email already exists!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            conn.close()


    def clear_form(self):
        self.name_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.password_entry.delete(0, END)
        self.age_entry.delete(0, END)
        self.phone_entry.delete(0, END)
        self.address_entry.delete("1.0", END)
        self.gender_var.set('')
        self.terms_var.set(False)
        self.profile_label.config(image='', text="Click to add\nprofile picture")
        self.profile_image = None
        self.strength_var.set("Weak")
        self.strength_label.config(fg="red")
        self.education_entry.delete(0, END)
        self.reg_number = self.generate_registration_number()
        self.reg_entry.config(state='normal')
        self.reg_entry.delete(0, END)
        self.reg_entry.insert(0, self.reg_number)
        self.reg_entry.config(state='readonly')
if __name__ == "__main__":
    root = Tk()
    app = RegistrationForm(root)
    root.mainloop()