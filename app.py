from backend.controllers.openalpr_recognizer import OpenALPRDetector
from backend.controllers.plate_recognizer import PlateRecognizerAPI
from backend.controllers.base_plate_recognizer import BasePlateRecognizer

detector = OpenALPRDetector()
imagem_teste = "/data/backend/assets/image1.jpg"

placas = detector.find_plate(imagem_teste)

print(f'Busca local: {placas}')

detector = PlateRecognizerAPI()
imagem_teste = "backend/assets/image1.jpg"

placas = detector.find_plate(imagem_teste)

print(f'Busca API: {placas}')