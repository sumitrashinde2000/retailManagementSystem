import sqlite3
from flask import Flask,render_template,request, url_for,flash,redirect
from werkzeug.exceptions import abort

app = Flask(__name__)
app.secret_key = "manbearpig_MHGJHJ898"

@app.route("/hello")
def index():
    flash("whats your name?")
    return render_template("index.html")

@app.route("/greet" , methods=["POST","GET"])
def greet():
    flash("Hi " + str(request.form['name_input']) + ", great to see you!")
    return render_template("index.html")

@app.route('/products')
def get_products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall( )
    conn.close()
    return render_template('index.html', products=products)

def get_db_connection():
    conn = sqlite3.connect('database.retail')
    conn.row_factory = sqlite3.Row
    return conn

def get_code(code_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?',(code_id)).fetchone()
    conn.close()
    if product is None:
        abort(404)
        return product
    
@app.route('/<int:code_id>')
def product(code_id):
    product = get_code(code_id)
    return render_template('post.html',product=product) 

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        code = request.form['code']
        name = request.form['name']
        category = request.form['category']
        purchaseDate = request.form['purchaseDate']
        expiryDate = request.form['expiryDate']

        if not code:
            flash("Code is required")
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO products(code,name,category) VALUES (?, ?, ?)' ,('PRD0001', 'Parachute hair oil 250ML', 'Beauty & Hair care'))  
            conn.commit()
            conn.close()     
        return render_template('create.html')

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    product = get_code(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!' .format(product['code'])) 
    return redirect(url_for('index'))   
