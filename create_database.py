import sqlite3

def create_database():
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    
    # Create recipes table
    # (id, title, ingredients, instructions, image_path)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recipes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        ingredients TEXT NOT NULL,
        instructions TEXT NOT NULL,
        image_path TEXT
    )
    """)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
