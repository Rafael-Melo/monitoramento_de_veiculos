from backend.models import db
from datetime import datetime

class VeiculoDetectado(db.Model):
    __tablename__ = 'veiculos_detectados'

    id = db.Column(db.Integer, primary_key=True)
    caminho_imagem = db.Column(db.String, nullable=False)
    placa_original = db.Column(db.String)
    placa_corrigida = db.Column(db.String)
    placa_valida = db.Column(db.Boolean)
    xmin = db.Column(db.Integer)
    xmax = db.Column(db.Integer)
    ymin = db.Column(db.Integer)
    ymax = db.Column(db.Integer)
    data = db.Column(db.DateTime(), default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('caminho_imagem', 'placa_original', name='uix_imagem_placa'),
    )