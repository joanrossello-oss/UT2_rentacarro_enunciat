from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Carros(db.Model):
    __tablename__ = "carros"
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    clase = db.Column(db.Enum("basic","1cavall","2cavalls", name="clase"), nullable=False)
    preu = db.Column(db.Float, nullable=False)
    descripcio = db.Column(db.String(250))
    img = db.Column(db.String(50),default="carro1.png")
    reservas = db.relationship("Reservas", back_populates="carro", cascade="delete-orphan") 
    def to_dict(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "clase": self.clase,
            "preu": self.preu,
            "descripcio": self.descripcio,
            "img": self.img,
            "reservas": self.reservas
        }

class Reservas(db.Model):
    __tablename__ = "reservas"
    inicireserva = db.Column(db.DateTime, primary_key=True,  default=datetime.now, nullable=False)
    finalreserva = db.Column(db.DateTime, default=datetime.now, nullable=False)
    usuario = db.Column(db.String(150), nullable=False)
    idcarro = db.Column(db.Integer, db.ForeignKey("carros.id"), primary_key=True)
    carro = db.relationship("Carros", back_populates="reservas")
    def to_dict(self):
        return {
            "idcarro": self.idcarro,
            "iniciReserva": self.inicireserva,
            "finalReserva": self.finalreserva,
            "usuario": self.usuario,
            "carro": self.carro
        }