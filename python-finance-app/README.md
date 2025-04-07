
# 💸 Osobní finance – Python aplikace s MySQL a Tkinter

Tato aplikace umožňuje uživatelům sledovat své finanční transakce pomocí jednoduchého grafického rozhraní (Tkinter) a databáze MySQL.

---

## 🧰 Požadavky

- Python 3.10+ (doporučeno)
- Lokální MySQL server
- pip pro správu balíčků
- Vytvořená databáze: `personal_finance`
- Uživatelský účet (např. `root`) s přístupem k databázi
- `.env` soubor s přihlašovacími údaji

---

## 📦 Instalace

1. **Klonuj repozitář:**

```bash
git clone https://github.com/tvoje-repo/python-finance-app.git
cd python-finance-app
```

2. **Vytvoř `.env` soubor:**

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=heslo
DB_NAME=personal_finance
```

3. **Nainstaluj závislosti:**

```bash
pip install -r requirements.txt
```

---

## 🗄️ Nastavení databáze

1. Spusť MySQL:

```bash
mysql -u root -p
```

2. Vytvoř databázi:

```sql
CREATE DATABASE personal_finance;
```

3. Spusť aplikaci – vytvoří tabulky automaticky:

```bash
python main.py
```

---

## 🧑‍💻 Funkce aplikace

### Běžný uživatel:
- Registrace / přihlášení
- Přidávání a mazání transakcí
- Zobrazení zůstatku


### 👑 Admin uživatel:
- Zobrazení všech uživatelů a jejich transakcí
- Možnost mazat uživatele

---

##  Testovací admin účet

```text
Uživatelské jméno: admin
Heslo: admin123
```

Pokud účet neexistuje, vytvoř ho ručně:

```python
from models.user import User
from database.database_manager import DatabaseManager

db = DatabaseManager()
db.connect_to_database()
admin = User(db)
admin.register("admin", "admin@example.com", "admin123")
db.close()
```

---

##  Struktura projektu

```
python-finance-app/
├── main.py
├── .env
├── requirements.txt
├── config/
│   └── db_config.py
├── database/
│   └── database_manager.py
├── models/
│   ├── user.py
│   └── transaction.py
└── gui/
    ├── app_gui.py
    ├── login_screen.py
    ├── dashboard.py
    └── admin_dashboard.py
```

---

##  Použité technologie

- Python
- Tkinter
- MySQL
- bcrypt
- python-dotenv

