import sqlite3
from flask import Flask,render_template,request, url_for,flash,redirect
from werkzeug.exceptions import abort

app = Flask(__name__)
app.secret_key = "retail_XYYGJ746"

@app.route('/')
def index():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall( )
    conn.close()
    return render_template('index.html', products=products)

def get_db_connection():
    conn = sqlite3.connect('database.retail')
    conn.row_factory = sqlite3.Row
    return conn

def get_product(product_code):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE code = ?',(product_code,)).fetchone()
    conn.close()
    if product is None:
        abort(404)
    return product
    
@app.route('/<code>')
def product(code):
    product = get_product(code)
    return render_template('product.html',product=product) 

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
            conn.execute('INSERT INTO products(code,name,category,purchaseDate,expiryDate) VALUES (?, ?, ?, ?, ?)', (code,name,category,purchaseDate,expiryDate))  
            conn.commit()
            conn.close()  
            return redirect(url_for('index'))   
    return render_template('create.html')

@app.route('/<code>/edit', methods=('GET', 'POST'))
def edit(code):
    product = get_product(code)

    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        purchaseDate = request.form['purchaseDate']
        expiryDate = request.form['expiryDate']

        if not name:
            flash('Name is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE products SET name = ?, category = ?, purchaseDate = ?, expiryDate = ? '
                         ' WHERE code = ?',
                         (name, category, purchaseDate, expiryDate, code))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', product=product)

@app.route('/<code>/delete', methods=('POST',))
def delete(code):
    product = get_product(code)
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE code = ?', (code,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!' .format(product['code'])) 
    return redirect(url_for('index'))   