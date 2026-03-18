import sqlite3

try:
    conn = sqlite3.connect('db.sqlite3', timeout=10)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS "budgets_companysettings" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "total_company_budget" decimal NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("Table created successfully.")
except Exception as e:
    print("Error:", e)
