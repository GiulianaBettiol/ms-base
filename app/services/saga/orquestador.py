
from typing import Dict, Any, List, Optional
from app.services.saga.acciones import SagaAction
from app.utils.logger_config import setup_logger


logger = setup_logger(__name__)


class SagaOrchestrator:
  
    _DATOS_INDICES = {
        0: "pago",
        1: "compra",
        2: "stock",
    }

    def __init__(self, acciones: List[SagaAction], datos: Dict[str, Any]):
        
        self.acciones = acciones
        self.datos = datos.copy()
        self.ids_generados: List[Optional[str]] = []
        self.respuesta = {
            "mensaje": "OK",
            "codigo_estado": 201,
            "datos": {"mensaje": "Operación realizada con éxito"},
        }

    def ejecutar(self) -> Dict[str, Any]:
     
        saga_datos = self.datos.copy()

        for indice, accion in enumerate(self.acciones):
            try:
                logger.info(f"Ejecutando acción {indice + 1}/{len(self.acciones)}")
                
                
                tipo_datos = self._DATOS_INDICES.get(indice)
                if not tipo_datos or tipo_datos not in saga_datos:
                    raise ValueError(
                        f"Datos faltantes para acción {indice}: esperado '{tipo_datos}'"
                    )
                
                datos_accion = saga_datos[tipo_datos]
                
                
                url, respuesta_datos = accion.ejecutar(datos_accion)
                
                
                id_generado = respuesta_datos.get("datos", {}).get("id")
                self.ids_generados.append(id_generado)
                logger.info(f"Acción {indice + 1} exitosa. ID generado: {id_generado}")
                
                
                codigo_estado = respuesta_datos.get("codigo_estado", 201)
                if codigo_estado not in (200, 201):
                    self.respuesta["codigo_estado"] = codigo_estado
                    self.respuesta["mensaje"] = respuesta_datos.get("mensaje", "Error desconocido")
                    self.respuesta["datos"] = respuesta_datos.get("datos", {})
                    self._compensar(indice)
                    return self.respuesta
                    
            except Exception as e:
                logger.error(f"Error en acción {indice + 1}: {str(e)}")
                self.respuesta["codigo_estado"] = 500
                self.respuesta["mensaje"] = "Error durante la ejecución de la saga"
                self.respuesta["datos"] = {"error": str(e)}
                self._compensar(indice)
                return self.respuesta

        logger.info(f"Saga completada exitosamente. IDs generados: {self.ids_generados}")
        return self.respuesta

    def _compensar(self, indice: int) -> None:
       
        logger.warning(f"Iniciando compensación desde acción {indice}")
        
        try:
            for i in range(indice - 1, -1, -1):
                if i >= len(self.acciones):
                    logger.warning(f"Índice {i} fuera de rango de acciones")
                    continue
                    
                accion = self.acciones[i]
                id_recurso = self.ids_generados[i] if i < len(self.ids_generados) else None
                
                if not id_recurso:
                    logger.warning(f"No hay ID disponible para compensar acción {i + 1}")
                    continue
                
                try:
                    exito = accion.compensar(id_recurso)
                    if exito:
                        logger.info(f"Compensación exitosa para acción {i + 1} (ID: {id_recurso})")
                    else:
                        logger.warning(f"Compensación parcial para acción {i + 1} (ID: {id_recurso})")
                except Exception as e:
                    logger.error(f"Error compensando acción {i + 1}: {str(e)}")
                    
        except Exception as e:
            logger.exception(f"Error crítico en compensación: {str(e)}")
