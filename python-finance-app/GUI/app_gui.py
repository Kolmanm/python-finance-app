# gui/app_gui.py

import tkinter as tk
from GUI.login_screen import LoginScreen
from GUI.dashboard import Dashboard

class FinanceAppGUI:
    def __init__(self, root, db):
        self.root = root
        self.root.title("💸 Personal Finance App")
        self.db = db
        self.user = None

        self.login_screen = LoginScreen(self.root, self, db)

    def on_login_success(self, user):
        self.user = user
        self.login_screen.destroy()

        if user.username == "admin":
            from GUI.admin_dashboard import AdminDashboard
            self.dashboard = AdminDashboard(self.root, self, self.db)
        else:
            from GUI.dashboard import Dashboard
            self.dashboard = Dashboard(self.root, self, self.db, self.user)

    def logout(self):
        self.dashboard.destroy()
        self.__init__(self.root, self.db)