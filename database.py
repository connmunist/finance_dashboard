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