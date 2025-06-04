from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import init_db, create_user, verify_user, get_user
from utils import generate_dynamic_token, verify_dynamic_token

app = Flask(__name__)
app.secret_key = 'clave-supersecreta'  # Mejor usar variable de entorno en producción

init_db()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/consultar_token', methods=['GET', 'POST'])
def consultar_token():
    if request.method == 'POST':
        token = request.form.get('token')
        user_id = verify_dynamic_token(token)
        if user_id:
            user = get_user(user_id)
            return render_template('estado_publico.html', user=user)
        else:
            flash("Token inválido o expirado.")
    return render_template('consultar_token.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form

        email = data['email']
        password = data['password']
        nombre = data['nombre']
        estado_vih = data['estado_vih']
        ultima_prueba_fecha = data.get('ultima_prueba_fecha') or None
        ultima_carga_viral = data.get('ultima_carga_viral') or None
        cd4_actual = data.get('cd4_actual')
        tratamiento_actual = data.get('tratamiento_actual') or None
        en_control_medico = 'en_control_medico' in data  # Checkbox: presente = True

        # Validar CD4 solo si fue proporcionado
        cd4_valor = int(cd4_actual) if cd4_actual else None

        if create_user(email, password, nombre, estado_vih,
                       ultima_prueba_fecha, ultima_carga_viral,
                       cd4_valor, tratamiento_actual, en_control_medico):
            flash("Registro exitoso. Inicia sesión.")
            return redirect(url_for('login'))
        else:
            flash("Correo ya registrado.")
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = verify_user(request.form['email'], request.form['password'])
        if user_id:
            session['user_id'] = user_id
            return redirect(url_for('dashboard'))
        else:
            flash("Credenciales inválidas")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = get_user(session['user_id'])
    return render_template('dashboard.html', user=user)

@app.route('/generate_token')
def generate_token():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    token = generate_dynamic_token(session['user_id'])
    return render_template('token.html', token=token)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5055)
