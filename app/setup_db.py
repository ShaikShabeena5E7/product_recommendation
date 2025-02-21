import sqlite3

# Connect to SQLite database (creates file if it doesn't exist)
conn = sqlite3.connect("test.db")
cursor = conn.cursor()

# Create products table
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT NOT NULL,
    price REAL NOT NULL
)
""")

# Insert sample product data
products = [
    ("Wireless Headphones", "Electronics", "Noise-canceling wireless headphones with long battery life.", 150),
    ("Smartwatch", "Wearable Tech", "Waterproof smartwatch with heart rate monitoring and GPS.", 200),
    ("Yoga Mat", "Fitness", "Eco-friendly non-slip yoga mat for all fitness levels.", 50),
    ("Resistance Bands", "Fitness", "Set of resistance bands for home workouts.", 30)
]

cursor.executemany("INSERT INTO products (name, category, description, price) VALUES (?, ?, ?, ?)", products)
conn.commit()
conn.close()

print("Database setup complete! Products added.")
