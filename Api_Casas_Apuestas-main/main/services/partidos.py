import sys
sys.path.insert(0,"C:/Users/Lorenzo/Documents/programacion/2.Desarrollo_OO/Apuestas_UEFA/Api_Casas_Apuestas-main/repositories")
sys.path.insert(0,"C:/Users/Lorenzo/Documents/programacion/2.Desarrollo_OO/Apuestas_UEFA/Api_Casas_Apuestas-main/map")

from repositoriopartido import PartidoRepositorio
from partido_schema import PartidoSchema 



partido_schema =PartidoSchema()
partido_repositorio = PartidoRepositorio()

class PartidoService:

    def obtener_partidos(self):
        return partido_repositorio.find_all()

    def obtener_partido_por_id(self, id):
        return partido_repositorio.find_one(id)

    def eliminar_partido(self, id):
        return partido_repositorio.delete(id)

    def actualizar_partido(self, id, data):
        partido = self.obtener_partido_por_id(id)
        for key, value in data.items():
            partido.__setattr__(key, value)
        return partido_repositorio.update(objeto=partido)

    def agregar_partido(self, partido):
            return partido_repositorio.create(partido)


