import os
import sys
import time
import psycopg2

DB_CONFIG: dict[str, str] = {
    "host": os.environ["DB_HOST"],
    "port": os.environ["DB_PORT"],
    "dbname": os.environ["DB_NAME"],
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASSWORD"],
}


def wait_for_db(retries: int = 10, delay: int = 3) -> None:
    for attempt in range(1, retries + 1):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            conn.close()
            print("Database connection established.")
            return
        except psycopg2.OperationalError as e:
            print(f"Attempt {attempt}/{retries}: Database not ready — {e}")
            time.sleep(delay)
    print("Could not connect to the database after maximum retries. Exiting.")
    sys.exit(1)


if __name__ == "__main__":
    wait_for_db()