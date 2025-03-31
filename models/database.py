from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()       

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    tipo = db.Column(db.String(150))

    def __init__(self, nome, tipo):
        self.nome = nome
        self.tipo = tipo
