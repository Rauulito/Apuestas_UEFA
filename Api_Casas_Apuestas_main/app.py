from main import create_app, db
import os
from faker import Faker
from main.models import ClienteModel, EquipoModel, PartidoModel
import csv
from main.services.cuota import CuotaService
from main.map import CuotaSchema

cuota_schema = CuotaSchema()
service_cuota = CuotaService()

app = create_app()

app.app_context().push()

fake = Faker('es_ES')


def load_clientes():
    for _ in range(100):
        cliente = ClienteModel(nombre=fake.first_name(), apellido=fake.last_name(), email=fake.email())
        db.session.add(cliente)
        db.session.commit()
    db.session.close()


def load_equipos():
    with open('./docs/equipo.csv', encoding='utf-8') as csv_file:
        try:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                equipo = EquipoModel(nombre=row[0], escudo=row[1], pais=row[2], puntaje=float(row[3]))
                db.session.add(equipo)
                db.session.commit()
            db.session.close()
        except:
            db.session.rollback()


def load_partidos():
    formato = "%d/%m/%Y %H:%M"
    with open('./docs/partidos.csv', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            partido = PartidoModel(equipo_local_id=row[1], equipo_visitante_id=row[2])
            db.session.add(partido)
            db.session.commit()


def load_cuotas():
    partidos = db.session.query(PartidoModel).all()
    xx = 0 # PARA VER COMO EVOLUCIONA LA EJECUCION
    for partido in partidos:
        json = {
            "partido_id": partido.id
        }
        cuota = cuota_schema.load(json)
        # Cambiamos la siguiente sentencia por el nuevo metodo de calcular cuotas afinado que hemos
        # creado en el servicio de cuotas
        #service_cuota.aplicar_cuotas(cuota)
        service_cuota.aplicar_cuotas_afinado(cuota)
        xx = xx + 1 # PARA VER COMO EVOLUCIONA LA EJECUCION
        print("Voy por:", xx, "cuota local=", cuota.cuota_local, "cuota visitante=", cuota.cuota_visitante,
                "cuota empate=", cuota.cuota_empate) # PARA VER COMO EVOLUCIONA LA EJECUCION
        db.session.add(cuota)
        db.session.commit()


if __name__ == '__main__':

    print("Programa iniciado")
    db.create_all()
    print("Creado todo")
    load_clientes()
    print("Cargados los clientes")
    load_equipos()
    print("Cargados los equipos")
    load_partidos()
    print("Cargados los partidos")
    load_cuotas()
    print("Cargadas las cuotas")

    #app.run(port=os.getenv("PORT"), debug=True)
