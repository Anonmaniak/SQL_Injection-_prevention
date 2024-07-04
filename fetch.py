import tkinter as tk
import sqlite3

def add_entry():
    # Get user inputs from the entry fields
    name = name_entry.get()
    age = age_entry.get()

    # Input validation
    if not name or not age:
        status_label.config(text="Name and Age are required")
        return

    try:
        # Convert age to integer
        age = int(age)
    except ValueError:
        status_label.config(text="Age must be a number")
        return

    # Connect to the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Use a prepared statement to prevent SQL injection
    query = "INSERT INTO users (name, age) VALUES (?, ?)"
    cursor.execute(query, (name, age))
    conn.commit()

    status_label.config(text="Entry added successfully")

    # Close the connection
    conn.close()

def fetch_entries():
    # Connect to the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Fetch data from the database
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    # Display data in the UI
    data_text.delete(1.0, tk.END)  # Clear previous data
    for row in rows:
        data_text.insert(tk.END, f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}\n")

    # Close the connection
    conn.close()

# Create the main window
root = tk.Tk()
root.title("SQL Injection Prevention")

# Create entry fields and labels
tk.Label(root, text="Name:").grid(row=0, column=0)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1)

tk.Label(root, text="Age:").grid(row=1, column=0)
age_entry = tk.Entry(root)
age_entry.grid(row=1, column=1)

# Add buttons
submit_button = tk.Button(root, text="Add Entry", command=add_entry)
submit_button.grid(row=2, column=0, columnspan=2)

fetch_button = tk.Button(root, text="Fetch Entries", command=fetch_entries)
fetch_button.grid(row=3, column=0, columnspan=2)

# Status label
status_label = tk.Label(root, text="")
status_label.grid(row=4, column=0, columnspan=2)

# Text widget to display fetched data
data_text = tk.Text(root, height=10, width=40)
data_text.grid(row=5, column=0, columnspan=2)

# Create SQLite database table
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')
conn.commit()
conn.close()

# Start the GUI application
root.mainloop()
