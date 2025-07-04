from flask import Flask, request, jsonify
from pathlib import Path
from dotenv import load_dotenv
import uuid
import os
from backend.controllers.openalpr_recognizer import OpenALPRDetector
from backend.controllers.plate_recognizer import PlateRecognizerAPI
import mimetypes

dotenv_path = Path(__file__).parents[1].joinpath('.env').as_posix()
load_dotenv(dotenv_path=dotenv_path)

from flask_migrate import Migrate
from backend.models import db
from backend.models.database_model import VeiculoDetectado

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
db.init_app(app)
migrate = Migrate(
    app=app,
    db=db,
    directory=Path(__file__).parents[0].joinpath('migrations').as_posix()
)

@app.route('/detectar-placa', methods=['POST'])
def detectar_placa():
    if "imagem" not in request.files:
        return jsonify({'error': 'Arquivo de imagem não enviado'}), 400
    
    imagem = request.files["imagem"]

    extensao = Path(imagem.filename).suffix
    nome_arquivo = f"{uuid.uuid4()}{extensao}"
    caminho_arquivo = Path('assets').joinpath(nome_arquivo).as_posix()
    # caminho_arquivo = Path(__file__).parents[0].joinpath('assets', nome_arquivo).as_posix()

    imagem.save(caminho_arquivo)

    mimetype, _ = mimetypes.guess_type(caminho_arquivo)

    detector = OpenALPRDetector()
    # detector = PlateRecognizerAPI()
    
    if mimetype.startswith('image'):
        resultados = detector.find_plate(caminho_imagem=caminho_arquivo)
    elif mimetype.startswith('video') and hasattr(detector, 'find_plate_in_video'):
        resultados = detector.find_plate_in_video(caminho_arquivo, 30)
    else:
        return jsonify({'error': 'Não é possível fazer a detecção nesse tipo de arquivo'}), 400

    if resultados:
        return jsonify({'success': resultados}), 200
    
    return jsonify({'error': 'Placa não detectada na imagem'}), 404

if __name__ == '__main__':
    app.run()