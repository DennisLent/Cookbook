from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import sqlite3
import os

app = Flask(__name__)

#global configs
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    connection = sqlite3.connect('cookbook.db')
    connection.row_factory = sqlite3.Row
    return connection

#pages

#homepage
@app.route("/")
def homepage():
    connection = get_db_connection()
    recipes = connection.execute("SELECT * FROM recipes").fetchall()
    connection.close()
    print("this worked")
    return render_template("home.html", recipes=recipes)

#new recipe
@app.route("/new")
def new_recipe():
    if request.method == "POST":
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        file = request.files['image']
        image_path = None
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(image_path)

        conn = get_db_connection()
        conn.execute('INSERT INTO recipes (title, ingredients, instructions, image_path) VALUES (?, ?, ?, ?)',
                     (title, ingredients, instructions, image_path))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('new_recipe.html')


if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)