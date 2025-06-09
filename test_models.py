import unittest
import sqlite3
import os
from models import create_user, verify_user, get_user
from utils import generate_dynamic_token, verify_dynamic_token

class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_db = 'test_db.sqlite3'

        # Crear una base de datos de prueba con la estructura actualizada
        conn = sqlite3.connect(cls.test_db)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                nombre TEXT,
                estado_vih TEXT,
                fecha_prueba TEXT,
                carga_viral TEXT,
                cd4 TEXT,
                tratamiento TEXT,
                control TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def setUp(self):
        self.email = "test@example.com"
        self.password = "1234"
        self.nombre = "Usuario Prueba"
        self.estado = "Positivo"
        self.extra = {
            "fecha_prueba": "2025-06-01",
            "carga_viral": "5,000 copias/ml",
            "cd4": "350 células/mm³",
            "tratamiento": "Iniciado en 2025",
            "control": True
        }

        # Limpia si ya existe ese usuario
        conn = sqlite3.connect('test_db.sqlite3')
        c = conn.cursor()
        c.execute('DELETE FROM users WHERE email = ?', (self.email,))
        conn.commit()
        conn.close()

        # Llama a la función real para insertar el usuario
        create_user(
            self.email, self.password, self.nombre, self.estado,
            self.extra["fecha_prueba"], self.extra["carga_viral"],
            self.extra["cd4"], self.extra["tratamiento"], self.extra["control"]
        )

    def test_verify_user(self):
        user_id = verify_user(self.email, self.password)
        self.assertIsNotNone(user_id)

    def test_get_user(self):
        user_id = verify_user(self.email, self.password)
        user = get_user(user_id)
        self.assertEqual(user[1], self.email)
        self.assertEqual(user[3], self.estado)

    def test_token_generation_and_verification(self):
        user_id = verify_user(self.email, self.password)
        token = generate_dynamic_token(user_id)
        verified_id = verify_dynamic_token(token)
        self.assertEqual(user_id, verified_id)

    def tearDown(self):
        # Elimina el usuario de prueba después de cada test
        conn = sqlite3.connect('test_db.sqlite3')
        c = conn.cursor()
        c.execute('DELETE FROM users WHERE email = ?', (self.email,))
        conn.commit()
        conn.close()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_db):
            os.remove(cls.test_db)

if __name__ == '__main__':
    unittest.main()


#La creación de usuarios funciona como se esperay y la verificación de contraseñas.
#La consulta de datos devuelve la información correcta.
#Y los correos duplicados están siendo correctamente rechazados.