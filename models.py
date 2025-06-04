import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def init_db():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            nombre TEXT,
            estado_vih TEXT,
            ultima_prueba_fecha TEXT,
            ultima_carga_viral TEXT,
            cd4_actual INTEGER,
            tratamiento_actual TEXT,
            en_control_medico INTEGER
        )
    ''')
    conn.commit()
    conn.close()
    insertar_usuarios_demo()


def create_user(email, password, nombre, estado_vih, ultima_prueba_fecha=None,
                ultima_carga_viral=None, cd4_actual=None,
                tratamiento_actual=None, en_control_medico=False):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    hashed = generate_password_hash(password)
    try:
        c.execute('''
            INSERT INTO users (
                email, password, nombre, estado_vih,
                ultima_prueba_fecha, ultima_carga_viral,
                cd4_actual, tratamiento_actual, en_control_medico
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (email, hashed, nombre, estado_vih, ultima_prueba_fecha,
              ultima_carga_viral, cd4_actual, tratamiento_actual,
              int(en_control_medico)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def verify_user(email, password):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('SELECT id, password FROM users WHERE email = ?', (email,))
    result = c.fetchone()
    conn.close()
    if result and check_password_hash(result[1], password):
        return result[0]
    return None


def get_user(user_id):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('''
        SELECT id, email, nombre, estado_vih, ultima_prueba_fecha,
               ultima_carga_viral, cd4_actual, tratamiento_actual, en_control_medico
        FROM users WHERE id = ?
    ''', (user_id,))
    user = c.fetchone()
    conn.close()
    return user


def insertar_usuarios_demo():
    usuarios_demo = [
        # email, password, nombre, estado, fecha, carga, cd4, tratamiento, en control
        ("ana@example.com", "1234", "Ana Gómez", "Negativo", "2024-04-01", None, None, None, False),
        ("luis@example.com", "abcd", "Luis Rojas", "Positivo", "2024-03-15", "Indetectable", 520, "TLD", True),
        ("carla@example.com", "pass", "Carla Ruiz", "Negativo", "2024-05-10", None, None, None, False),
        ("david@example.com", "secret", "David Pérez", "Positivo", "2024-01-20", "Detectable", 320, "AZT/3TC/NVP", True),
    ]
    for u in usuarios_demo:
        create_user(*u)



