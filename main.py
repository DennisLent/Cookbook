from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import sqlite3
import os
from utils.tags import generate_tags

app = Flask(__name__)

#global configs
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

#secret key needed to update database
#doesn't matter if it is here, there is no sensitive data involved
app.secret_key = "hello"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    connection = sqlite3.connect('recipes.db')
    connection.row_factory = sqlite3.Row
    return connection

#pages

#homepage
@app.route("/")
def homepage():
    connection = get_db_connection()
    recipes = connection.execute("SELECT * FROM recipes").fetchall()
    connection.close()

    all_tags = set()
    for recipe in recipes:
        tags = recipe['tags'].split(', ')
        all_tags.update(tags)

    return render_template("home.html", recipes=recipes, all_tags=sorted(all_tags))

#new recipe
@app.route("/new",methods=('GET', 'POST'))
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
        
        tags = generate_tags(ingredients=ingredients)

        conn = get_db_connection()
        conn.execute('INSERT INTO recipes (title, ingredients, instructions, image_path, tags) VALUES (?, ?, ?, ?, ?)',
                     (title, ingredients, instructions, image_path, tags))
        conn.commit()
        conn.close()
        
        return redirect(url_for('homepage'))
    
    return render_template('new_recipe.html')

#recipes
@app.route("/recipe/<int:recipe_id>")
def recipe_page(recipe_id):
    connection = get_db_connection()
    recipe = connection.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,)).fetchone()
    connection.close()
    if recipe is None:
        return "Recipe not found!", 404
    
    # Split ingredients and instructions into lists
    ingredients = recipe['ingredients'].split('\n')
    instructions = recipe['instructions'].split('\n')

    return render_template("recipe.html", recipe=recipe, ingredients=ingredients, instructions=instructions)

# Edit recipe
@app.route("/edit/<int:recipe_id>", methods=('GET', 'POST'))
def edit_recipe(recipe_id):
    connection = get_db_connection()
    recipe = connection.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,)).fetchone()

    if request.method == "POST":
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']

        connection.execute('UPDATE recipes SET title = ?, ingredients = ?, instructions = ? WHERE id = ?',
                           (title, ingredients, instructions, recipe_id))
        connection.commit()
        connection.close()

        flash('Recipe updated successfully!')
        return redirect(url_for('recipe_page', recipe_id=recipe_id))

    connection.close()
    return render_template('edit.html', recipe=recipe)

# Delete recipe
@app.route("/delete/<int:recipe_id>", methods=['POST'])
def delete_recipe(recipe_id):
    connection = get_db_connection()
    connection.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    connection.commit()
    connection.close()
    flash('Recipe deleted successfully!')
    return redirect(url_for('homepage'))

if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)