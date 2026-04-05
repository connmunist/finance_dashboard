import sqlite3                        # Python's built-in SQLite library — no install needed

DB_PATH = "finance.db"               # The filename of our database. One constant, used everywhere.
                                      # If you ever rename it, you change it in exactly one place.

def get_connection():
    """Opens and returns a connection to the database file."""
    return sqlite3.connect(DB_PATH)   # If finance.db doesn't exist, SQLite creates it automatically

def initialize_database():
    """Creates tables if they don't already exist. Safe to call every time the app starts."""
    conn = get_connection()           # Open the conversation channel
    cursor = conn.cursor()            # Get the executor

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            date        TEXT NOT NULL,
            amount      REAL NOT NULL,
            category    TEXT NOT NULL,
            description TEXT
        )
    """)
    # INTEGER PRIMARY KEY AUTOINCREMENT — SQLite assigns id automatically. You never set it manually.
    # TEXT / REAL / INTEGER — SQLite's data types. REAL means decimal number (like 47.82).
    # NOT NULL — this field is required. SQLite will reject a row without it.
    # description has no NOT NULL — it's optional. A transaction can have no note.

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS income (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            pay_date TEXT NOT NULL,
            amount   REAL NOT NULL
        )
    """)

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS ebt_refills (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                refill_date TEXT NOT NULL,
                amount      REAL NOT NULL
        )
    """)

    conn.commit()                     # Save the changes to disk
    conn.close()                      # Close the conversation — always clean up after yourself

def add_transaction(date, amount, category, description =""):
    """Save a new transaction (EBT or personal) to the database."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions (date, amount, category, description) 
        VALUES (?, ?, ?, ?)
    """, (date, amount, category, description))

    conn.commit()
    conn.close()

def add_income(pay_date, amount):
    """Save a new income payment to the database."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO income (pay_date, amount)
        VALUES (?, ?) 
    """, (pay_date, amount))

    conn.commit()
    conn.close()

def add_ebt_refill(refill_date, amount):
    """Save a new EBT refill to the database."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO ebt_refills (refill_date, amount)
        VALUES (?,?)
    """, (refill_date, amount))

    conn.commit()
    conn.close()

def get_monthly_spending(category, year, month):
    """Return total spending for a given category in a given month."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE category = ?
        AND strftime('%Y', date) = ?
        AND strftime('%m', date) = ?
    """, (category, str(year), str(month).zfill(2)))

    result = cursor.fetchone()
    conn.close()
    return result[0]

def get_latest_ebt_refill():
    """Return latest EBT refill"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT refill_date, amount
        FROM ebt_refills
        ORDER BY refill_date DESC LIMIT 1
                   """)
    
    result = cursor.fetchone()
    conn.close()
    return result

def get_all_transactions():
    """Return every transaction as a list, newest first."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date, amount, category, description
        FROM transactions
        ORDER BY date DESC
    """)

    results = cursor.fetchall()
    conn.close()
    return results

def get_monthly_income(year, month):
    """Return total income received in a given month."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM income
        WHERE strftime('%Y', pay_date) = ?
        AND strftime('%m', pay_date) = ?
    """, (str(year), str(month).zfill(2)))

    result = cursor.fetchone()
    conn.close()
    return result[0]