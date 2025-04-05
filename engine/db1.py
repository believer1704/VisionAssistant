import csv
import sqlite3
import os

# Connect to the SQLite database
conn = sqlite3.connect('vision2.db')
cursor = conn.cursor()

# Create the sys_command table if it doesn't exist
query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)

# Create the contacts table if it doesn't exist

cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (
    id integer primary key, 
    name VARCHAR(200), 
    mobile_no VARCHAR(255), 
    email VARCHAR(255) NULL
)''')

# Uncomment the line below to clear the contacts table before inserting new data
#cursor.execute("DELETE FROM contacts")
# conn.commit()

# Specify the column indices you want to import from the CSV (0-based index)
#desired_columns_indices = [0,2]  # Adjust if you need to select other columns

# Read data from the CSV file and insert it into the database
#with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
    #csvreader = csv.reader(csvfile)
    #for row in csvreader:
        #Print row length for debugging
        #print(f"Row length: {len(row)} - Row data: {row}")
        
        # Skip rows with insufficient columns
        #if len(row) < max(desired_columns_indices) + 1:
            #print(f"Skipping row: {row} (insufficient columns)")
            #continue
        
         #Select the desired columns
        #selected_data = [row[i] for i in desired_columns_indices]

        # Insert data into the contacts table
        #cursor.execute('''INSERT INTO contacts (id, name, mobile_no) VALUES (null, ?, ?)''', tuple(selected_data))

# Commit changes and close the connection
#conn.commit()
#conn.close()

#query = "INSERT INTO contacts VALUES (null,'anisha', '+91 89783 00500','null')"
#query = query.strip().lower()
#cursor.execute(query)
#conn.commit()
# Uncomment and use the lines below to test queries on the contacts table
#query = "anisha "
#query = query.strip().lower()
#cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
#results = cursor.fetchall()
#if results:
    #print(results[0][0])
#else:
    #print("No matching records found.")
#conn.close()
