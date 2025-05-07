import requests
from pprint import pprint
from base_plate_recognizer import standardize_plate, validate_plate

API_KEY = '0f8e6ef80b5a78dc4ec10ccdb4764aa4d46df347'
url = 'https://api.platerecognizer.com/v1/plate-reader/'
headers = {'Authorization': f'Token {API_KEY}'}

# with open(r"C:\Users\rmelo\Documents\TESTES PYTHON\FLET\monitoramento_de_veiculos\backend\assets\image1.jpg", "rb") as image_file:
#     files = {'upload': image_file}
#     response = requests.post(url, headers=headers, files=files)

def find_plate(caminho_imagem):
    try:
        with open(caminho_imagem, "rb") as image_file:
            files = {"upload": image_file}
            response = requests.post(url, headers=headers, files=files)
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
        corrected_plate = standardize_plate(original_plate)
        valid_plate = validate_plate(corrected_plate)

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

fp = find_plate(r"C:\Users\rmelo\Documents\TESTES PYTHON\FLET\monitoramento_de_veiculos\backend\assets\image2.jpg")

pprint(fp)
