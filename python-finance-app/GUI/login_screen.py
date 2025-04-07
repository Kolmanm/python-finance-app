# gui/login_screen.py

import tkinter as tk
from tkinter import messagebox
from models.user import User

class LoginScreen:
    def __init__(self, root, app, db):
        self.root = root
        self.app = app
        self.db = db
        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack()

        self.mode = "login"  # or "register"

        self.build_form()

    def build_form(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        tk.Label(self.frame, text="Username").grid(row=0, column=0, sticky="w")
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.grid(row=0, column=1)

        tk.Label(self.frame, text="Password").grid(row=1, column=0, sticky="w")
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.grid(row=1, column=1)

        if self.mode == "register":
            tk.Label(self.frame, text="Email").grid(row=2, column=0, sticky="w")
            self.email_entry = tk.Entry(self.frame)
            self.email_entry.grid(row=2, column=1)

        btn_text = "Login" if self.mode == "login" else "Register"
        action = self.login if self.mode == "login" else self.register

        self.submit_btn = tk.Button(self.frame, text=btn_text, command=action)
        self.submit_btn.grid(row=3, columnspan=2, pady=10)

        switch_text = "No account? Register" if self.mode == "login" else "Have an account? Login"
        self.switch_btn = tk.Button(self.frame, text=switch_text, fg="blue", command=self.toggle_mode)
        self.switch_btn.grid(row=4, columnspan=2)

    def toggle_mode(self):
        self.mode = "register" if self.mode == "login" else "login"
        self.build_form()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = User(self.db)
        if user.login(username, password):
            self.destroy()
            self.app.on_login_success(user)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()

        user = User(self.db)
        if user.register(username, email, password):
            messagebox.showinfo("Success", "Account created! You can now log in.")
            self.toggle_mode()
        else:
            messagebox.showerror("Error", "Failed to register user, check all inputs! ")

    def destroy(self):
        self.frame.destroy()