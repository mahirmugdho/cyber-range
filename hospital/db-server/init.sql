-- Create tables
CREATE TABLE IF NOT EXISTS staff (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS patients (
    id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    dob TEXT NOT NULL,
    diagnosis TEXT NOT NULL,
    physician TEXT NOT NULL
);

-- Seed staff accounts
INSERT INTO staff (username, password, role) VALUES
    ('doctor1', 'password123', 'Doctor'),
    ('nurse1', 'nursepass', 'Nurse'),
    ('admin1', 'adminpass', 'Administrator')
ON CONFLICT (username) DO NOTHING;

-- Seed patient records
INSERT INTO patients (first_name, last_name, dob, diagnosis, physician) VALUES
    ('John', 'Smith', '1981-04-12', 'Hypertension', 'Dr. Patel'),
    ('Maria', 'Lopez', '1992-09-30', 'Asthma', 'Dr. Kim'),
    ('David', 'Brown', '1975-01-18', 'Type 2 Diabetes', 'Dr. Chen'),
    ('Aisha', 'Rahman', '2000-06-07', 'Migraine', 'Dr. Patel'),
    ('Emily', 'Davis', '1988-11-22', 'Anemia', 'Dr. Lewis'),
    ('James', 'Wilson', '1965-03-30', 'Coronary Artery Disease', 'Dr. Chen'),
    ('Sofia', 'Martinez', '1990-07-14', 'Lupus', 'Dr. Kim'),
    ('Liam', 'Johnson', '2001-12-01', 'Appendicitis', 'Dr. Patel'),
    ('Fatima', 'Al-Hassan', '1978-09-19', 'Breast Cancer', 'Dr. Lewis'),
    ('Noah', 'Thompson', '1955-05-23', 'Chronic Kidney Disease', 'Dr. Chen'),
    ('Olivia', 'Garcia', '1983-11-08', 'Multiple Sclerosis', 'Dr. Kim'),
    ('Ethan', 'Lee', '1995-02-17', 'Appendicitis', 'Dr. Patel'),
    ('Ava', 'Nguyen', '1970-06-25', 'Osteoporosis', 'Dr. Lewis'),
    ('Marcus', 'Robinson', '1988-04-03', 'HIV/AIDS', 'Dr. Chen'),
    ('Priya', 'Patel', '2003-08-11', 'Epilepsy', 'Dr. Kim')
ON CONFLICT DO NOTHING;