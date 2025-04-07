from tkinter import Tk
from GUI.app_gui import FinanceAppGUI
from database.database_manager import DatabaseManager

db = DatabaseManager()
db.connect_to_server()
db.create_database_if_not_exists()
db.connect_to_database()
db.initialize_tables()

root = Tk()
app = FinanceAppGUI(root, db)
root.mainloop()

db.close()