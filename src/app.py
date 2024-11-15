from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_mysqldb import MySQL
from config import config

app = Flask(__name__)

db = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtener datos del formulario
        email = request.form['email']
        password = request.form['password']

        cur = db.connection.cursor()
        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        cur.execute(query, (email, password))
        user = cur.fetchone()
        cur.close()

        try:
            # Vereficar en la base de datos
            if user:
                # Inicio de sesion exitoso
                flash('¡Inicio de sesion exitoso!', 'success')
                return redirect(url_for('index'))
            else:
                # Inicio de sesion fallido
                flash('No puede ingresar, intente nuevamente', 'danger')
                return redirect(url_for('register'))
        except Exception as e:
            flash(str(e), 'danger')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Obtener datos del formulario
        fullname = request.form['fullname']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        try:
            # Insertar en la base de datos
            cur = db.connection.cursor()
            query = "INSERT INTO users (fullname, username, email, password) VALUES (%s, %s, %s, %s)"
            cur.execute(query, (fullname, username, email, password))
            db.connection.commit()
            cur.close()
            flash('¡Registro exitoso! Por favor, inicia sesión.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error al registrar: {e}', 'danger')
            db.connection.rollback()

    return render_template('register.html')

# Inicializar el carrito


@app.before_request
def init_cart():
    if 'cart' not in session:
        session['cart'] = []

# Agregar un producto al carrito


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product = request.json  # Suponemos que el producto viene en formato JSON
    session['cart'].append(product)
    session.modified = True  # Asegura que los cambios se guarden en la sesión
    return {'status': 'success'}

# Página para mostrar el carrito


@app.route('/cart')
def show_cart():
    cart_items = session.get('cart', [])
    return render_template('cart.html', cart=cart_items)


@app.route('/remove_from_cart/<item_id>', methods=['POST'])
def remove_from_cart(item_id):
    try:
        cart = session.get('cart', [])
        updated_cart = [item for item in cart if str(
            item['id']) != str(item_id)]
        session['cart'] = updated_cart
        session.modified = True
        return '', 204
    except Exception as e:
        return {'error': str(e)}, 500
    
@app.route('/process_payment', methods=['POST'])
def process_payment():
    try:
        # Aquí podrías integrar con una API de pago (e.g., Stripe o PayPal)
        session['cart'] = []  # Vaciar el carrito después del pago
        session.modified = True
        flash('¡Pago realizado con éxito!', 'success')
        return redirect(url_for('show_cart'))
    except Exception as e:
        flash(f'Error al procesar el pago: {e}', 'danger')
        return redirect(url_for('show_cart'))


# @app.errorhandler(404)
# def not_found(error):
#     return render_template('error-404.html'), 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()
