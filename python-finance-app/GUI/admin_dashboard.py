# gui/admin_dashboard.py

import tkinter as tk
from tkinter import messagebox

class AdminDashboard:
    def __init__(self, root, app, db):
        self.root = root
        self.app = app
        self.db = db

        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="👑 Admin Dashboard", font=("Helvetica", 16)).pack()

        self.user_listbox = tk.Listbox(self.frame, width=60)
        self.user_listbox.pack(pady=10)

        tk.Button(self.frame, text="Show Transactions for Selected User", command=self.show_user_transactions).pack()
        tk.Button(self.frame, text="Delete Selected User", command=self.delete_user).pack(pady=(5, 10))
        tk.Button(self.frame, text="Logout", command=self.logout).pack()

        self.tx_text = tk.Text(self.frame, height=15, width=80)
        self.tx_text.pack(pady=10)

        self.load_users()

    def load_users(self):
        self.user_listbox.delete(0, tk.END)
        self.users = self.db.fetch_all("SELECT * FROM users ORDER BY username")
        for user in self.users:
            self.user_listbox.insert(tk.END, f"{user['id']} | {user['username']} | {user['email']}")

    def show_user_transactions(self):
        selected = self.user_listbox.curselection()
        if not selected:
            return
        user = self.users[selected[0]]
        txs = self.db.fetch_all("SELECT * FROM transactions WHERE user_id = %s ORDER BY date DESC", (user["id"],))
        
        self.tx_text.delete("1.0", tk.END)
        self.tx_text.insert(tk.END, f"Transactions for {user['username']}:\n\n")
        for tx in txs:
            date_str = tx['date'].strftime("%Y-%m-%d %H:%M")
            self.tx_text.insert(tk.END, f"{date_str} | {tx['amount']}€ | {tx['category']} | {tx['description']}\n")

    def delete_user(self):
        selected = self.user_listbox.curselection()
        if not selected:
            return
        user = self.users[selected[0]]

        confirm = messagebox.askyesno("Confirm Delete", f"Delete user {user['username']}?")
        if confirm:
            self.db.execute_query("DELETE FROM users WHERE id = %s", (user["id"],))
            self.load_users()
            self.tx_text.delete("1.0", tk.END)
            messagebox.showinfo("Deleted", f"User {user['username']} has been deleted.")

    def logout(self):
        self.app.logout()

    def destroy(self):
        self.frame.destroy()