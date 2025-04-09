import pandas as pd
import sqlite3
import os
import logging

# set up logging
logging.basicConfig(filename='error_log.txt', level=logging.ERROR)

def infer_sqlite_type(value):
    """Infer SQLite column type from a sample value."""
    if pd.isna(value):
        return "TEXT"
    elif isinstance(value, int):
        return "INTEGER"
    elif isinstance(value, float):
        return "REAL"
    else:
        return "TEXT"
    
def table_exists(cursor, table_name):
    """Check if a table already exists in the database."""
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
    return cursor.fetchone() is not None
    
def create_table_from_csv(csv_path, db_path, table_name):
    try:
        # Load CSV
        df = pd.read_csv(csv_path)

        # Connect to DB
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check for conflict
        original_table_name = table_name
        if table_exists(cursor, table_name):
            print(f"Table '{table_name}' already exists.")
            choice = input("Do you want to [O]verwrite, [R]ename, or [S]kip? ").strip().upper()

            if choice == "S":
                print(f"⏭ Skipping '{csv_path}'.")
                return
            elif choice == "R":
                suffix = 1
                while table_exists(cursor, f"{table_name}_{suffix}"):
                    suffix += 1
                table_name = f"{table_name}_{suffix}"
                print(f"Renamed table to '{table_name}'.")
            elif choice == "O":
                cursor.execute(f"DROP TABLE IF EXISTS {original_table_name}")
                print(f"🧹 Dropped old table '{original_table_name}'.")
            else:
                print("Invalid choice. Skipping.")
                return

        # Build CREATE TABLE
        sample_row = df.iloc[0]
        columns = []
        for col in df.columns:
            inferred_type = infer_sqlite_type(sample_row[col])
            col_clean = col.strip().replace(" ", "_")
            columns.append(f"{col_clean} {inferred_type}")

        column_definitions = ", ".join(columns)
        create_stmt = f"CREATE TABLE {table_name} ({column_definitions});"
        cursor.execute(create_stmt)

        # Insert data
        df.columns = [col.strip().replace(" ", "_") for col in df.columns]
        df.to_sql(table_name, conn, if_exists="append", index=False)

        print(f"Successfully created table '{table_name}' from '{csv_path}'.")

    except Exception as e:
        logging.error(f"Error processing {csv_path}: {e}")
        print(f"Failed to process {csv_path}. Check error_log.txt for details.")

    finally:
        conn.close()

def list_tables(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("📋 Tables in the database:")
    for t in tables:
        print(f"  - {t[0]}")

def run_cli():
    db_path = "my_database.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("Welcome to your AI-powered Data Assistant!")
    print("Type 'help' to see available commands.\n")

    while True:
        user_input = input("What would you like to do? ").strip().lower()

        if user_input == "help":
            print("""
 Available commands:
  load         → Load a CSV file into the database
  list         → List current tables
  query        → Run a SQL query
  exit         → Exit the program
""")
        elif user_input == "load":
            csv_path = input("Enter CSV file path: ").strip()
            table_name = input("Enter table name: ").strip()
            create_table_from_csv(csv_path, db_path, table_name)

        elif user_input == "list":
            list_tables(cursor)

        elif user_input == "query":
            query = input("Enter your SQL query: ").strip()
            try:
                result = cursor.execute(query)
                rows = result.fetchall()
                for row in rows:
                    print(row)
            except Exception as e:
                logging.error(f"SQL Error: {e}")
                print(f"Error running query. See error_log.txt.")

        elif user_input == "exit":
            print("Goodbye!")
            break
        else:
            print("Unknown command. Type 'help' to see options.")

    conn.close()

if __name__ == "__main__":
    run_cli()

