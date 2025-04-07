# gui/dashboard.py

import tkinter as tk
from tkinter import messagebox
from models.transaction import Transaction

class Dashboard:
    def __init__(self, root, app, db, user):
        self.root = root
        self.app = app
        self.db = db
        self.user = user
        self.tx = Transaction(self.db)

        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text=f"Welcome, {self.user.username}!", font=("Helvetica", 16)).pack(pady=(0, 10))
        # Total balance label
        self.balance_var = tk.StringVar()
        self.balance_label = tk.Label(self.frame, textvariable=self.balance_var, font=("Helvetica", 14, "bold"), fg="green")
        self.balance_label.pack(pady=(0, 10))
        # Transaction list
        self.tx_listbox = tk.Listbox(self.frame, width=80)
        self.tx_listbox.pack(pady=10)

        self.load_transactions()

     # Amount
        tk.Label(self.frame, text="Castka (€)").pack(anchor="w")
        self.amount_entry = tk.Entry(self.frame)
        self.amount_entry.pack(pady=2)

        # Category
        tk.Label(self.frame, text="Kategorie").pack(anchor="w")
        self.category_entry = tk.Entry(self.frame)
        self.category_entry.pack(pady=2)

        # Description
        tk.Label(self.frame, text="Info").pack(anchor="w")
        self.description_entry = tk.Entry(self.frame)
        self.description_entry.pack(pady=2)

        tk.Button(self.frame, text="Pridej Transakci", command=self.add_transaction).pack(pady=5)
        tk.Button(self.frame, text="Smaz transakcio", command=self.delete_selected).pack(pady=5)

        tk.Button(self.frame, text="Odhlasit!", command=self.logout).pack(pady=(20, 0))

    def load_transactions(self):
        self.tx_listbox.delete(0, tk.END)
        self.transactions = self.tx.get_all_for_user(self.user.id)

        total = 0.0
        for idx, tx in enumerate(self.transactions):
            total += float(tx['amount'])
            date_str = tx['date'].strftime("%Y-%m-%d %H:%M")
            text = f"{date_str} | {tx['amount']}€ | {tx['category']} | {tx['description'] or ''}"
            self.tx_listbox.insert(tk.END, text)

            # 🔴 Color red if amount is negative
            if tx['amount'] < 0:
                self.tx_listbox.itemconfig(idx, {'fg': 'red'})

        self.balance_var.set(f"Stav uctu: {total:.2f} €")
        self.balance_label.config(fg="green" if total >= 0 else "red")
        self.tx_listbox.delete(0, tk.END)
        self.transactions = self.tx.get_all_for_user(self.user.id)

        total = 0.0

        for tx in self.transactions:
                total += float(tx['amount'])
                date_str = tx['date'].strftime("%Y-%m-%d %H:%M")
                text = f"{date_str} | {tx['amount']}€ | {tx['category']} | {tx['description'] or ''}"
                self.tx_listbox.insert(tk.END, text)   

        self.balance_var.set(f"Current Balance: {total:.2f} €")
        self.balance_label.config(fg="green" if total >= 0 else "red")
        self.tx_listbox.delete(0, tk.END)
        self.transactions = self.tx.get_all_for_user(self.user.id)
        for tx in self.transactions:
                date_str = tx['date'].strftime("%Y-%m-%d %H:%M")
                text = f"{date_str} | {tx['amount']}€ | {tx['category']} | {tx['description'] or ''}"
                self.tx_listbox.insert(tk.END, text)
    
    def add_transaction(self):
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Amount must be a number.")
            return

        category = self.category_entry.get()
        description = self.description_entry.get()

        self.tx.add(self.user.id, amount, category, description)
        self.load_transactions()

    def delete_selected(self):
        selected_index = self.tx_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Select something", "Please select a transaction to delete.")
            return

        tx_to_delete = self.transactions[selected_index[0]]
        confirm = messagebox.askyesno("Confirm", "Delete this transaction?")
        if confirm:
            self.tx.delete(tx_to_delete["id"], self.user.id)
            self.load_transactions()

    def destroy(self):
        self.frame.destroy()

    def logout(self):
        self.app.logout()