import unittest
import time
from utils import generate_dynamic_token, verify_dynamic_token

class TestTokenUtils(unittest.TestCase):

    def test_generate_and_verify_token(self):
        user_id = 123

        # Genera un token válido por 1 minuto
        token = generate_dynamic_token(user_id, duration_minutes=1)
        self.assertIsInstance(token, str)
        
        # Verifica el token inmediatamente (debería ser válido)
        result = verify_dynamic_token(token)
        self.assertEqual(result, user_id)

        # Espera 2 minutos para que expire el token y falle la verificación
        time.sleep(2 * 60)
        result_expired = verify_dynamic_token(token)
        self.assertIsNone(result_expired)

    def test_verify_invalid_token(self):
        invalid_token = "token_invalido"
        result = verify_dynamic_token(invalid_token)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
