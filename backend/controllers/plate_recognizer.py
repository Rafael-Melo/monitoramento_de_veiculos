import requests
from pprint import pprint
from base_plate_recognizer import BasePlateRecognizer
from pathlib import Path
from dotenv import load_dotenv
import os

dotenv_path = Path(__file__).parents[2].joinpath('.env')
load_dotenv(dotenv_path=str(dotenv_path))

class PlateRecognizerAPI(BasePlateRecognizer):
    def __init__(self):
        self.api_key = os.getenv('API_KEY')
        self.url = 'https://api.platerecognizer.com/v1/plate-reader/'
        self.headers = {'Authorization': f'Token {self.api_key}'}

    def find_plate(self, caminho_imagem):
        try:
            with open(caminho_imagem, "rb") as image_file:
                files = {"upload": image_file}
                response = requests.post(self.url, headers=self.headers, files=files)
        except Exception as e:
            print(f"Erro ao abrir ou enviar a imagem: {e}")
            return []
        
        if not response.ok:
            print(f"Erro na requisição: {response.status_code}")
        
        results = response.json().get('results', [])
        detected_plates = []

        for result in results:
            original_plate = result.get('plate', '')
            box = result.get('box', {})
            corrected_plate = self._standardize_plate(original_plate)
            valid_plate = self._validate_plate(corrected_plate)

            detected_plates.append({
                "caminho_imagem": caminho_imagem,
                "placa_original": original_plate,
                "placa_corrigida": corrected_plate,
                "placa_valida": valid_plate,
                "xmin": box.get('xmin'),
                "ymin": box.get('ymin'),
                "xmax": box.get('xmax'),
                "ymax": box.get('ymax'),
            })
        
        return detected_plates

