import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Create the table
cursor.execute('''
CREATE TABLE IF NOT EXISTS ExampleTable (
    id INTEGER,
    name TEXT
)
''')

# Insert data into the table
cursor.executemany('''
INSERT INTO ExampleTable (id, name) VALUES (?, ?)
''', [
    (1, 'Alice'),
    (1, 'Bob'),
    (2, 'Charlie'),
    (3, 'Alice'),
    (3, 'Alice'),
    (3, 'David')
])

# Commit the changes
conn.commit()

# Query to find IDs with multiple associated names
query = '''
SELECT id
FROM ExampleTable
GROUP BY id
HAVING COUNT(DISTINCT name) > 1
'''

# Execute the query
cursor.execute(query)
results = cursor.fetchall()

# Print the results
print("IDs with multiple associated names:")
for row in results:
    print(row[0])

# Close the connection
conn.close()