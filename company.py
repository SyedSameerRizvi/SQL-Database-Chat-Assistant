import sqlite3

# Connect to SQLite database
connection = sqlite3.connect("employee.db")

# Create a cursor object
cursor = connection.cursor()

# Create the employees table
table_info = """
CREATE TABLE EMPLOYEES (
    NAME VARCHAR(50),
    DEPARTMENT VARCHAR(50),
    POSITION VARCHAR(50),
    SALARY REAL,
    HIRE_DATE DATE
)
"""

cursor.execute(table_info)

# Insert records into the EMPLOYEES table
insert_queries = [
    ("Ahmed Khan", "Sales", "Sales Manager", 75000.00, "2020-03-15"),
    ("Fatima Noor", "HR", "HR Coordinator", 60000.00, "2019-07-01"),
    ("Muhammad Ali", "IT", "Software Engineer", 95000.00, "2021-01-20"),
    ("Ayesha Karim", "Finance", "Accountant", 67000.00, "2018-05-11"),
    ("Bilal Saeed", "Marketing", "SEO Specialist", 72000.00, "2022-04-25"),
    ("Hassan Raza", "Sales", "Sales Executive", 50000.00, "2021-11-10"),
    ("Zainab Bukhari", "Operations", "Operations Manager", 82000.00, "2017-09-05"),
    ("Yusuf Qasim", "IT", "Data Analyst", 72000.00, "2020-12-08"),
    ("Imran Malik", "Finance", "Financial Analyst", 68000.00, "2019-10-22"),
    ("Mariam Zafar", "HR", "HR Manager", 80000.00, "2016-03-29"),
    ("Saad Hashmi", "IT", "DevOps Engineer", 87000.00, "2021-06-17"),
    ("Nadia Jamil", "Marketing", "Content Strategist", 69000.00, "2019-12-19"),
    ("Usman Farooq", "Operations", "Logistics Coordinator", 64000.00, "2020-08-07"),
    ("Hamza Tariq", "Finance", "Tax Consultant", 73000.00, "2021-09-28"),
    ("Sana Ahmed", "Sales", "Account Manager", 66000.00, "2022-01-13")
]

# Execute insert queries
cursor.executemany("INSERT INTO EMPLOYEES (NAME, DEPARTMENT, POSITION, SALARY, HIRE_DATE) VALUES (?, ?, ?, ?, ?)", insert_queries)

# Display all the records
print("The inserted employee records are:")
data = cursor.execute("SELECT * FROM EMPLOYEES")
for row in data:
    print(row)

# Commit changes and close the connection
connection.commit()
connection.close()