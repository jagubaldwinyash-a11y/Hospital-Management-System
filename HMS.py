import mysql.connector

# Connect to the database
# Make sure to change these credentials to match your local MySQL setup
mycon = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="jnv",
    auth_plugin="mysql_native_password"
)
cursor = mycon.cursor()

# Function to initialize database
def initialize_database():
    # Create patients table
    cursor.execute("DROP TABLE IF EXISTS patients")
    cursor.execute("""
    CREATE TABLE patients (
        pid INT PRIMARY KEY,
        pname VARCHAR(100) NOT NULL,
        pcell VARCHAR(15) NOT NULL
    );
    """)

    # Create doctors table
    cursor.execute("DROP TABLE IF EXISTS doctors")
    cursor.execute("""
    CREATE TABLE doctors (
        did INT PRIMARY KEY,
        dname VARCHAR(100) NOT NULL,
        dcell VARCHAR(15) NOT NULL
    );
    """)

    # Create appointments table
    cursor.execute("DROP TABLE IF EXISTS appointments")
    cursor.execute("""
    CREATE TABLE appointments (
        tid INT PRIMARY KEY,
        pid INT,
        did INT,
        fees FLOAT NOT NULL,
        Adate DATE NOT NULL,
        FOREIGN KEY (pid) REFERENCES patients(pid),
        FOREIGN KEY (did) REFERENCES doctors(did)
    );
    """)

    # Insert dummy data
    cursor.execute("""
    INSERT INTO patients (pid, pname, pcell) VALUES
    (1, 'John Doe', '1234567890'),
    (2, 'Jane Smith', '9876543210'),
    (3, 'Alice Johnson', '4567891230'),
    (4, 'Bob Brown', '7890123456'),
    (5, 'Emily Davis', '8901234567');
    """)

    cursor.execute("""
    INSERT INTO doctors (did, dname, dcell) VALUES
    (1, 'Dr. Smith', '1122334455'),
    (2, 'Dr. Johnson', '2233445566'),
    (3, 'Dr. Williams', '3344556677'),
    (4, 'Dr. Brown', '4455667788'),
    (5, 'Dr. Taylor', '5566778899');
    """)

    cursor.execute("""
    INSERT INTO appointments (tid, pid, did, fees, Adate) VALUES
    (1, 1, 1, 150.0, '2024-12-01'),
    (2, 2, 2, 200.0, '2024-12-02'),
    (3, 3, 3, 250.0, '2024-12-03'),
    (4, 4, 4, 300.0, '2024-12-04'),
    (5, 5, 5, 350.0, '2024-12-05');
    """)

    mycon.commit()
    print("Database initialized successfully!")

# Call the initialize_database function at the start
initialize_database()

# Display functions
def displaypatients():
    sql = "SELECT * FROM patients"
    cursor.execute(sql)
    results = cursor.fetchall()
    for c in results:
        pid = c[0]
        pname = c[1]
        pcell = c[2]
        print(f"Patient ID: {pid}, Patient Name: {pname}, Patient Cell: {pcell}")

def displaydoctors():
    sql = "SELECT * FROM doctors"
    cursor.execute(sql)
    results = cursor.fetchall()
    for c in results:
        did = c[0]
        dname = c[1]
        dcell = c[2]
        print(f"Doctor ID: {did}, Doctor Name: {dname}, Doctor Cell: {dcell}")

def displayappointments():
    sql = "SELECT * FROM appointments"
    cursor.execute(sql)
    results = cursor.fetchall()
    for c in results:
        tid = c[0]
        pid = c[1]
        did = c[2]
        fees = c[3]
        adate = c[4]
        print(f"Transaction ID: {tid}, Patient ID: {pid}, Doctor ID: {did}, Fees: {fees}, Appointment Date: {adate}")

# Add functions
def addpatient():
    print("Enter new patient details:")
    pid = int(input("Patient ID: "))
    pname = input("Patient Name: ")
    pcell = input("Patient Cell Number: ")
    sql = "INSERT INTO patients (pid, pname, pcell) VALUES (%s, %s, %s)"
    cursor.execute(sql, (pid, pname, pcell))
    mycon.commit()
    print("Patient added successfully!")

def adddoctor():
    print("Enter new doctor details:")
    did = int(input("Doctor ID: "))
    dname = input("Doctor Name: ")
    dcell = input("Doctor Cell Number: ")
    sql = "INSERT INTO doctors (did, dname, dcell) VALUES (%s, %s, %s)"
    cursor.execute(sql, (did, dname, dcell))
    mycon.commit()
    print("Doctor added successfully!")

def appointments():
    print("Enter appointment details:")
    tid = int(input("Transaction ID: "))
    pid = int(input("Patient ID: "))
    did = int(input("Doctor ID: "))
    fees = float(input("Fees: "))
    adate = input("Appointment Date (YYYY-MM-DD): ")
    sql = "INSERT INTO appointments (tid, pid, did, fees, Adate) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (tid, pid, did, fees, adate))
    mycon.commit()
    print("Appointment added successfully!")

# Delete function
def delete_entry(table_name, id_column):
    print(f"Delete entry from {table_name.capitalize()}")
    id_value = int(input(f"Enter {id_column.capitalize()} to delete: "))
    sql = f"DELETE FROM {table_name} WHERE {id_column} = %s"
    cursor.execute(sql, (id_value,))
    mycon.commit()
    print(f"Entry with {id_column} = {id_value} deleted successfully!")

# Menu-driven program
choice = 'Y'
while choice.lower() != 'n':
    print("\nWELCOME TO HOSPITAL MANAGEMENT SYSTEM\n")
    print("1. DISPLAY ALL PATIENTS DETAILS")
    print("2. DISPLAY ALL DOCTORS DETAILS")
    print("3. DISPLAY ALL APPOINTMENT DETAILS")
    print("4. ADD PATIENT DETAILS")
    print("5. ADD DOCTOR DETAILS")
    print("6. ADD APPOINTMENT DETAILS")
    print("7. DELETE PATIENT")
    print("8. DELETE DOCTOR")
    print("9. DELETE APPOINTMENT")
    
    c = int(input("Enter your choice (1-9): "))
    if c == 1:
        displaypatients()
    elif c == 2:
        displaydoctors()
    elif c == 3:
        displayappointments()
    elif c == 4:
        addpatient()
    elif c == 5:
        adddoctor()
    elif c == 6:
        appointments()
    elif c == 7:
        delete_entry("patients", "pid")
    elif c == 8:
        delete_entry("doctors", "did")
    elif c == 9:
        delete_entry("appointments", "tid")
    
    choice = input("Do you want to continue? (Y/N): ")

# Close the connection
cursor.close()
mycon.close()
