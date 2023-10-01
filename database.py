import sqlite3

# Create a connection to the database
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create a table for user information
c.execute('''CREATE TABLE users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              surname TEXT NOT NULL,
              email TEXT NOT NULL,
              password TEXT NOT NULL)''')

# Create a table for items
c.execute('''CREATE TABLE items
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              item_name TEXT NOT NULL,
              price REAL NOT NULL,
              description TEXT NOT NULL,
              user_id INTEGER NOT NULL,
              FOREIGN KEY (user_id) REFERENCES users(id))''')

# Create a table for photos
c.execute('''CREATE TABLE photos
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              filename TEXT NOT NULL,
              item_id INTEGER NOT NULL,
              FOREIGN KEY (item_id) REFERENCES items(id))''')



# Commit changes to the database
conn.commit()

