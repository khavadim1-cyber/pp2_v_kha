import csv
import psycopg2
from config import load_config

def get_connection():
    return psycopg2.connect(**load_config())

def create_table():
    sql = """
    CREATE TABLE IF NOT EXISTS phonebook (
        id       SERIAL PRIMARY KEY,
        name     VARCHAR(100) NOT NULL,
        phone    VARCHAR(20)  NOT NULL UNIQUE
    );
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
    print("Table 'phonebook' is ready.")

def insert_from_csv(filepath: str):
    sql = """
    INSERT INTO phonebook (name, phone)
    VALUES (%s, %s)
    ON CONFLICT (phone) DO UPDATE SET name = EXCLUDED.name;
    """
    inserted = 0
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [(row["name"].strip(), row["phone"].strip()) for row in reader]

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.executemany(sql, rows)
            inserted = cur.rowcount
        conn.commit()
    print(f"Inserted/updated {inserted} record(s) from '{filepath}'.")



def insert_from_console():
    name  = input("Enter name:  ").strip()
    phone = input("Enter phone: ").strip()
    sql = """
    INSERT INTO phonebook (name, phone)
    VALUES (%s, %s)
    ON CONFLICT (phone) DO UPDATE SET name = EXCLUDED.name;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (name, phone))
        conn.commit()
    print(f"Saved: {name} — {phone}")

def update_contact():
    print("Update by: 1) name  2) phone")
    choice = input("Choice: ").strip()

    if choice == "1":
        old_name = input("Current name: ").strip()
        new_name = input("New name:     ").strip()
        sql = "UPDATE phonebook SET name = %s WHERE name = %s;"
        params = (new_name, old_name)
    elif choice == "2":
        old_phone = input("Current phone: ").strip()
        new_phone = input("New phone:     ").strip()
        sql = "UPDATE phonebook SET phone = %s WHERE phone = %s;"
        params = (new_phone, old_phone)
    else:
        print("Invalid choice.")
        return

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.rowcount
        conn.commit()
    print(f"Updated {rows} record(s).")

def search_contacts():
    print("Search by: 1) name  2) phone prefix  3) show all")
    choice = input("Choice: ").strip()

    if choice == "1":
        name = input("Name (partial OK): ").strip()
        sql    = "SELECT id, name, phone FROM phonebook WHERE name ILIKE %s ORDER BY name;"
        params = (f"%{name}%",)
    elif choice == "2":
        prefix = input("Phone prefix: ").strip()
        sql    = "SELECT id, name, phone FROM phonebook WHERE phone LIKE %s ORDER BY phone;"
        params = (f"{prefix}%",)
    elif choice == "3":
        sql    = "SELECT id, name, phone FROM phonebook ORDER BY name;"
        params = ()
    else:
        print("Invalid choice.")
        return

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()

    if rows:
        print(f"\n{'ID':<6} {'Name':<25} {'Phone':<20}")
        print("-" * 52)
        for row in rows:
            print(f"{row[0]:<6} {row[1]:<25} {row[2]:<20}")
        print(f"\n{len(rows)} record(s) found.")
    else:
        print("No records found.")

def delete_contact():
    print("Delete by: 1) name  2) phone")
    choice = input("Choice: ").strip()

    if choice == "1":
        name = input("Name: ").strip()
        sql    = "DELETE FROM phonebook WHERE name = %s;"
        params = (name,)
    elif choice == "2":
        phone = input("Phone: ").strip()
        sql    = "DELETE FROM phonebook WHERE phone = %s;"
        params = (phone,)
    else:
        print("Invalid choice.")
        return

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.rowcount
        conn.commit()
    print(f"Deleted {rows} record(s).")

MENU = """
╔══════════════════════════════╗
║       PhoneBook Menu         ║
╠══════════════════════════════╣
║ 1. Import from CSV           ║
║ 2. Add contact (console)     ║
║ 3. Update contact            ║
║ 4. Search contacts           ║
║ 5. Delete contact            ║
║ 0. Exit                      ║
╚══════════════════════════════╝
"""

def main():
    create_table()
    while True:
        print(MENU)
        choice = input("Select option: ").strip()
        if choice == "1":
            path = input("CSV file path: ").strip()
            insert_from_csv(path)
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            update_contact()
        elif choice == "4":
            search_contacts()
        elif choice == "5":
            delete_contact()
        elif choice == "0":
            print("Bye!")
            break
        else:
            print("Unknown option, try again.")

if __name__ == "__main__":
    main()