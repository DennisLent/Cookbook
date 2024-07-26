import sqlite3

def create_database():
    conn = sqlite3.connect('cookbook.db')
    cursor = conn.cursor()
    
    # Create recipes table
    # (id, title, ingredients, instructions, image_path)
    cursor.execute("CREATE TABLE IF NOT EXISTS recipes(if, title, ingredients, instructions, image_path)")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
