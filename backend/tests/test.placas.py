import unittest
import os
import sys
from pathlib import Path

root = Path(__file__).parents[2]
sys.path.append(str(root))

from backend.controllers.base_plate_recognizer import BasePlateRecognizer

class BPR(BasePlateRecognizer):
    def find_plate(self):
        pass
    
class TestPlateRecognizer(unittest.TestCase):
    def test_standardize_plate(self):
        teste_cases = [
            ("A8C 1B23", "ABC1B23"),        # espaço no meio    
            ("A0C123", "AOC123"),           # 6 caracteres
            ("AB1123", "ABI123"),           # falta um caractere
            ("4BC1234", "ABC1234"),         # número no lugar da primeira letra
            ("A8C12B3", "ABC1283"),         # letra onde deveria ser número
            ("ABO1234", "ABO1234"),         # letra O onde deveria ser 0
            ("ABC123", "ABC123"),           # incompleta
            ("AIC1D23", "AIC1D23"),         # números 1 e letras trocadas
            ("A8C1D2", "ABC1D2"),           # 6 caracteres
            ("A*C1234", "ACI234"),          # caractere inválido
            ("A1C 1234", "AIC1234"),        # espaço no meio    
            ("ABC12S4", "ABC1254"),         # letra no final
            ("ABC12", "ABC12"),             # muito curta
            ("1234567", "IZ34567"),         # todos números
            ("A8C1D2@", "ABC1D2"),          # caractere especial
            ("AB 1234", "ABI234"),          # espaço entre letras e números
            ("A1C1D23", "AIC1D23"),         # mistura número/letra nas posições erradas
            ("ABZ12B3", "ABZ1283"),         # letra no lugar de número
            ("AB5I2S3", "ABS1253"),         # confusões comuns OCR (5=S, I=1, S=5)
            ("ABC12O4", "ABC1204"),         # O no final
            ("A8C123B", "ABC1238"),         # letra no final
            ("4B51234", "ABS1234"),         # número no lugar de letra
            ("A1C1B2", "AIC182"),           # muito curta
            ("AI01234", "AIO1234"),         # I no lugar de 1
            ("ABC1D2", "ABC1D2"),           # 6 caracteres, Mercosul quase certo
            ("A*C12D3", "ACI2D3"),          # caractere inválido no começo
            ("AB1D2S", "ABID25"),           # muito curta, com confusão
            ("ABO12S3", "ABO1253"),         # O por 0, S por 5
            ("ABC1S23", "ABC1S23"),         # letra S por 5
            ("AB4I23", "ABA123"),           # 6 caracteres, A por 4, I por 1
        ]

        isinstance = BPR()

        for placa_original, placa_esperada in teste_cases:
            with self.subTest(placa = placa_original):
                self.assertEqual(isinstance._standardize_plate(placa_original), placa_esperada)
    
    def teste_validate_plate(self):
        valid_plates = [
            "ABC1234",   # Brasileiro
            "ABC1B23",   # Mercosul
            "AIC1234",   # Brasileiro
            "AIC1D23",   # Mercosul
            "ABC1254",   # Brasileiro
            "ABO1253",   # Brasileiro
            "ABC1204",   # Brasileiro
            "ABC1238",   # Brasileiro
            "ABS1234",   # Brasileiro
            "AIO1234",   # Brasileiro
            "ABC1S23",   # Mercosul
        ]

        invalid_plates = [
            "AOC123", "ABI123", "ABC123", "ABC1D2", "ACI234", 
            "ABC12", "IZ34567", "ABI234", "AIC182", "ACI2D3", 
            "ABID25", "ABA123",
        ]

        isinstance = BPR()

        for placa in valid_plates:
            with self.subTest(placa = placa):
                self.assertTrue(isinstance._validate_plate(placa), msg=f'✅ {placa} deria ser valida')
        
        for placa in invalid_plates:
            with self.subTest(placa = placa):
                self.assertFalse(isinstance._validate_plate(placa), msg= f'❌ {placa} deria ser invalida')

if __name__ == '__main__':
    unittest.main()