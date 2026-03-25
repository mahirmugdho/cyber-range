import sqlite3

conn = sqlite3.connect("hospital.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS staff")
cur.execute("DROP TABLE IF EXISTS patients")

cur.execute("""
CREATE TABLE staff (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
""")

cur.execute("""
CREATE TABLE patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    dob TEXT NOT NULL,
    diagnosis TEXT NOT NULL,
    physician TEXT NOT NULL
)
""")

staff_data = [
    ("doctor1", "password123", "Doctor"),
    ("nurse1", "nursepass", "Nurse"),
    ("admin1", "adminpass", "Administrator")
]

patient_data = [
    ("John", "Smith", "1981-04-12", "Hypertension", "Dr. Patel"),
    ("Maria", "Lopez", "1992-09-30", "Asthma", "Dr. Kim"),
    ("David", "Brown", "1975-01-18", "Type 2 Diabetes", "Dr. Chen"),
    ("Aisha", "Rahman", "2000-06-07", "Migraine", "Dr. Patel"),
    ("Emily", "Davis", "1988-11-22", "Anemia", "Dr. Lewis")
]

cur.executemany(
    "INSERT INTO staff (username, password, role) VALUES (?, ?, ?)",
    staff_data
)

cur.executemany(
    "INSERT INTO patients (first_name, last_name, dob, diagnosis, physician) VALUES (?, ?, ?, ?, ?)",
    patient_data
)

conn.commit()
conn.close()

print("Database initialized with fake hospital data.")