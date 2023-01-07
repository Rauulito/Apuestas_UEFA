from .cliente import Cliente as ClienteModel
from .apuesta import Apuesta as ApuestaModel
from .empresa import Empresa as EmpresaModel
from .partido import Partido as PartidoModel
from .equipo import Equipo as EquipoModel
from .cuota import Cuota as CuotaModel


"""
IMPORTANTE--> ¿Cómo ejecutar todos estos archivos con las importaciones relativas incorporadas?
Desde un archivo bajo el cual sean conocidos los arhivos se ejecuta el siguiente comando:
python -m main.models."archivo a ejecutar"
De esta manera se evita el error:   "ImportError: attempted relative import with no known parent package"
"""