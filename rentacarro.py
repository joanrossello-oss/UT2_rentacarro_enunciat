from db import Carros, Reservas, db

# Carro

@staticmethod
def carrega_carros() -> list[dict]:
    carros = Carros.query.order_by(Carros.id).all()
    return [c.to_dict() for c in carros]

@staticmethod
def crear_carro(nom, descripcio, clase, preu):
    carro = Carros(
        nom=nom,
        descripcio=descripcio,
        clase=clase,
        preu=preu
    )
    db.session.add(carro)
    db.session.commit()

@staticmethod
def borrar_carros(id: int):
    carro = Carros.query.get(id)
    if carro:
        db.session.delete(carro)
        db.session.commit()

@staticmethod
def actualitzar_carros(id, nom, descripcio, clase, preu) -> None:
    carro = Carros.query.get(id)
    if carro:
        carro.nom = nom
        carro.descripcio = descripcio
        carro.clase = clase
        carro.preu = preu
        db.session.commit()

# Reserva

@staticmethod
def obtenir_reserves():
    reserva = Reservas.query.all()
    return [r.to_dict() for r in reserva]

@staticmethod
def crear_reserva(iniciReserva, finalReserva, usuario, idcarro):
    reserva = Reservas(
        idcarro=idcarro,
        iniciReserva=iniciReserva,
        finalReserva=finalReserva,
        usuario=usuario
    )
    db.session.add(reserva)
    db.session.commit()
