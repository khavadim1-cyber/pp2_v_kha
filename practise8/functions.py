import psycopg2
from config import load_config


def get_connection():
    return psycopg2.connect(**load_config())


def setup_database():
    sql = """
    CREATE TABLE IF NOT EXISTS suppliers (
        id    SERIAL PRIMARY KEY,
        name  VARCHAR(100) NOT NULL,
        phone VARCHAR(20)  NOT NULL UNIQUE
    );

    CREATE OR REPLACE FUNCTION search_suppliers(pattern TEXT)
    RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
    BEGIN
        RETURN QUERY
            SELECT s.id, s.name, s.phone
            FROM   suppliers s
            WHERE  s.name  ILIKE '%' || pattern || '%'
               OR  s.phone ILIKE '%' || pattern || '%'
            ORDER  BY s.name;
    END;
    $$ LANGUAGE plpgsql;

    CREATE OR REPLACE PROCEDURE upsert_user(p_name TEXT, p_phone TEXT)
    LANGUAGE plpgsql AS $$
    BEGIN
        INSERT INTO suppliers (name, phone)
        VALUES (p_name, p_phone)
        ON CONFLICT (phone)
        DO UPDATE SET name = EXCLUDED.name;
    END;
    $$;

    CREATE OR REPLACE PROCEDURE bulk_insert_users(
        p_names  TEXT[],
        p_phones TEXT[],
        OUT invalid_rows TEXT
    )
    LANGUAGE plpgsql AS $$
    DECLARE
        i       INT;
        p_name  TEXT;
        p_phone TEXT;
        bad     TEXT[] := '{}';
    BEGIN
        FOR i IN 1 .. array_length(p_names, 1) LOOP
            p_name  := p_names[i];
            p_phone := p_phones[i];

            IF p_phone ~ '^\+?[0-9]{10,15}$' THEN
                INSERT INTO suppliers (name, phone)
                VALUES (p_name, p_phone)
                ON CONFLICT (phone)
                DO UPDATE SET name = EXCLUDED.name;
            ELSE
                bad := array_append(bad, p_name || ' | ' || p_phone);
            END IF;
        END LOOP;

        IF array_length(bad, 1) IS NULL THEN
            invalid_rows := 'none';
        ELSE
            invalid_rows := array_to_string(bad, '; ');
        END IF;
    END;
    $$;

    CREATE OR REPLACE FUNCTION get_suppliers_page(p_limit INT, p_offset INT)
    RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
    BEGIN
        RETURN QUERY
            SELECT s.id, s.name, s.phone
            FROM   suppliers s
            ORDER  BY s.name
            LIMIT  p_limit
            OFFSET p_offset;
    END;
    $$ LANGUAGE plpgsql;

    CREATE OR REPLACE PROCEDURE delete_user(p_value TEXT)
    LANGUAGE plpgsql AS $$
    BEGIN
        DELETE FROM suppliers
        WHERE name = p_value OR phone = p_value;
    END;
    $$;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
    print("Database is ready.\n")


def search_contacts():
    pattern = input("Enter name or phone (or part of it): ").strip()
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM search_suppliers(%s);", (pattern,))
            rows = cur.fetchall()
    _print_table(rows)


def upsert_user():
    name  = input("Name:  ").strip()
    phone = input("Phone: ").strip()
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL upsert_user(%s, %s);", (name, phone))
        conn.commit()
    print("Done.")


def bulk_insert():
    print("Enter contacts one per line as:  Name,Phone")
    print("Empty line when finished.\n")
    names, phones = [], []
    while True:
        line = input("> ").strip()
        if not line:
            break
        parts = line.split(",", 1)
        if len(parts) != 2:
            print("  Format must be  Name,Phone  — skipped.")
            continue
        names.append(parts[0].strip())
        phones.append(parts[1].strip())

    if not names:
        print("Nothing to insert.")
        return

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "CALL bulk_insert_users(%s::text[], %s::text[], NULL);",
                (names, phones)
            )
            invalid = cur.fetchone()
        conn.commit()

    if invalid and invalid[0] != "none":
        print(f"\nInvalid entries (not saved):\n  {invalid[0]}")
    else:
        print("\nAll entries saved successfully.")


def paginated_view():
    try:
        limit = int(input("Records per page: ").strip())
        page  = int(input("Page number (1, 2, ...): ").strip())
    except ValueError:
        print("Please enter numbers.")
        return
    offset = (page - 1) * limit
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_suppliers_page(%s, %s);", (limit, offset))
            rows = cur.fetchall()
    print(f"\nPage {page}  (limit={limit}, offset={offset})")
    _print_table(rows)


def delete_user():
    value = input("Enter name or phone to delete: ").strip()
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL delete_user(%s);", (value,))
        conn.commit()
    print("Done.")


def _print_table(rows):
    if not rows:
        print("No records found.")
        return
    print(f"\n{'ID':<6} {'Name':<25} {'Phone':<20}")
    print("-" * 52)
    for row in rows:
        print(f"{row[0]:<6} {row[1]:<25} {row[2]:<20}")
    print(f"\n{len(rows)} record(s).")

MENU = """
╔══════════════════════════════════╗
║      Suppliers  (Practice 8)     ║
╠══════════════════════════════════╣
║ 1. Search by pattern             ║
║ 2. Add / update one contact      ║
║ 3. Bulk insert (with validation) ║
║ 4. View with pagination          ║
║ 5. Delete contact                ║
║ 0. Exit                          ║
╚══════════════════════════════════╝"""

def main():
    setup_database()
    while True:
        print(MENU)
        choice = input("Select option: ").strip()
        if   choice == "1": search_contacts()
        elif choice == "2": upsert_user()
        elif choice == "3": bulk_insert()
        elif choice == "4": paginated_view()
        elif choice == "5": delete_user()
        elif choice == "0": print("Bye!"); break
        else: print("Unknown option.")


if __name__ == "__main__":
    main()