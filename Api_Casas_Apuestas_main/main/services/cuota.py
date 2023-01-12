from main.repositories.repositoriocuota import CuotaRepositorio
from main.services.partidos import PartidoService
from main.services.equipo import EquipoService
from math import cos
import csv

repositorio = CuotaRepositorio()
partido_service = PartidoService()
equipo_service = EquipoService()

class CuotaService:

    def obtener_cuotas(self):
        return repositorio.find_all()

    def obtener_cuota(self, id):
        return repositorio.find_one(id)

    def agregar_cuota(self, cuota):
        self.aplicar_cuotas(cuota)
        return repositorio.create(cuota)

    def aplicar_cuotas(self, cuota) -> None:
        partido = partido_service.obtener_partido_por_id(cuota.partido_id)
        visitante = equipo_service.obtener_equipo_por_id(partido.equipo_visitante_id)
        local = equipo_service.obtener_equipo_por_id(partido.equipo_local_id)

        cuota.cuota_local = self.calcular_cuota(local.puntaje)
        cuota.cuota_visitante = self.calcular_cuota(visitante.puntaje)
        cuota.cuota_empate = self.calcular_cuota(self.calcular_empate(local.puntaje, visitante.puntaje))

    def calcular_base(self):
        return equipo_service.obtener_puntaje_mas_alto()

    def calcular_probabilidad(self, puntos):
        return puntos/self.calcular_base()

    def calcular_empate(self, puntos_local, puntos_visitante):
        return abs(puntos_local - puntos_visitante)

    def calcular_cuota(self, puntos):
        cuota_calculada = cos(self.calcular_probabilidad(puntos))
        cuota_calculada = (cuota_calculada * 10) - 4
        return round(cuota_calculada, 2)

    # Creamos una función afinada para calculo de las cuotas
    def aplicar_cuotas_afinado(self, cuota) -> None:
        partido = partido_service.obtener_partido_por_id(cuota.partido_id)
        visitante = equipo_service.obtener_equipo_por_id(partido.equipo_visitante_id)
        local = equipo_service.obtener_equipo_por_id(partido.equipo_local_id)

        # Asignamos los  puntos del año actual a los equipos del partido

        puntos_local = local.puntaje
        puntos_visitante = visitante.puntaje

        # Ajustamos los puntos de los equipos del partido teniendo en cuenta los datos
        # de años anteriores:
        # Leeremos los ficheros con los datos de los años anteriores, y tendremos en cuenta
        # los puntos de esos años ponderándolos según el año a los que pertenecen, de forma
        # que influyan más los más actuales y menos los más antiguos

        # Parámetros del modelo a tener en cuenta para actualizaciones y posible mejora
        # del modelo:
        #   Habría que actualizar el año cuando corresponda
        #   El peso se puede ajustar al alza o a la baja conforme a la experiencia que se vaya
        #   obteniendo con la ejecución del modelo y la comparación con los datos reales
        # (El modelo se puede ampliar incluyendo más ficheros con otros tipos de datos
        # a tener en cuenta para el ajusta de los puntos de los equipos, como podrían ser por ejemeplo:
        # los resultados de los últimos partidos entre ambos equipos, los goles que marcan cuando
        # juegan de local o de visitante, etc.)
        año_actual = 2021
        peso_diferencia_años = 0.18

        # Para ajustar los puntos con los de los años anteriores, tendremos en cuenta
        # los 5 años anteriores al actual
        # Para cada año:
        #     Buscamos a los equipos local y visitante en el fichero del año
        #     Cogemos los puntos que han obtenido en ese año
        #     Calculamos el peso del año en función del peso de su antigüedad
        #     Actualizamos los puntos del local y del visitante sumándoles los puntos
        #            obtenidos en el año que estamos tratando ponderado por el peso del año

        for i in range(5):
            año_datos = año_actual - (i + 1)
            año = str(año_datos)
            with open(f'./docs/equipo{año}.csv', encoding='utf-8') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    if local.nombre == row[0]:
                        puntos_local_año = float(row[3])
                    elif visitante.nombre == row[0]:
                        puntos_visitante_año = float(row[3])

                peso_año = 1 - (año_actual - año_datos) * peso_diferencia_años

                #EL SIGUIENTE PRINT ES PARA CONTROLAR QUE LOS CALCULOS SON CORRECTOS
                #print(peso_año, puntos_local, puntos_local_año, puntos_visitante, puntos_visitante_año)

                puntos_local = puntos_local + puntos_local_año * peso_año
                puntos_visitante = puntos_visitante + puntos_visitante_año * peso_año

        #EL SIGUIENTE PRINT ES PARA CONTROLAR QUE LOS CALCULOS SON CORRECTOS
        #print(puntos_local, puntos_visitante)

        probabilidades = self.calcular_probabilidad_afinada(puntos_local, puntos_visitante)
        probabilidad_local = probabilidades[0]
        probabilidad_visitante = probabilidades[1]
        probabilidad_empate = probabilidades[2]
        cuota.cuota_local = self.calcular_cuota_afinada(probabilidad_local)
        cuota.cuota_visitante = self.calcular_cuota_afinada(probabilidad_visitante)
        cuota.cuota_empate = self.calcular_cuota_afinada(probabilidad_empate)

    # Creamos una función afinada para calculo de las probabilidades
    def calcular_probabilidad_afinada(self, puntos_local, puntos_visitante):
        # Parámetros del modelo a tener en cuenta para actualizaciones y posible mejora
        # del modelo:
        #   El peso se puede ajustar al alza o a la baja conforme a la experiencia que se vaya
        #   obteniendo con la ejecución del modelo y la comparación con los datos reales
        peso_local = 2
        peso_visitante = 0.9
        peso_empate = 2
        puntos_empate = (puntos_local + puntos_visitante) / peso_empate
        puntos_total = peso_local * puntos_local + peso_visitante * puntos_visitante
        # Para que la suma de probabilidades de 1 la sentencia anterior sería de la siguiente forma:
        # puntos_total = peso_local * puntos_local + peso_visitante * puntos_visitante + puntos_empate
        # pero de esa forma las cuotas salen muy altas, así que de la misma forma que en la versión
        # inicial no ponemos esa restricción, y no tenemos en cuenta los puntos del empate. De esa forma
        # la suma de probabilidades es superior a 1 pero conseguimos unas cuotas no tan altas y mejoramos
        # el margen de la casa de apuestas
        probabilidad_local = peso_local * puntos_local / puntos_total
        probabilidad_visitante = peso_visitante * puntos_visitante / puntos_total
        probabilidad_empate = puntos_empate / puntos_total
        return (probabilidad_local, probabilidad_visitante, probabilidad_empate)

    # Creamos una función afinada para calculo de las cuotas en base a la probabilidad ya calculada
    # y manteniendo los criterios anteriores de cálculo de cuota en función de la probabilidad
    def calcular_cuota_afinada(self, probabilidad):
        cuota_calculada = cos(probabilidad)
        cuota_calculada = (cuota_calculada * 10) - 4
        return round(cuota_calculada, 2)

