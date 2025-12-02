
from typing import Dict, Any
from requests import Response

from app.utils.logger_config import setup_logger


logger = setup_logger(__name__)


class ServiceError(Exception):
    """Error genérico en operación de servicio."""
    pass


class ValidationError(ServiceError):
    """Error de validación de datos (422)."""
    pass


class NotFoundError(ServiceError):
    """Recurso no encontrado (404)."""
    pass


class ConflictError(ServiceError):
    """Conflicto en la operación (409)."""
    pass


class ServerError(ServiceError):
    """Error del servidor remoto (500+)."""
    pass


def validar_respuesta(response: Response, codigo_esperado: int = 200) -> None:
    
    if response.status_code == codigo_esperado:
        return

    
    error_map: Dict[int, tuple] = {
        404: (NotFoundError, "Recurso no encontrado."),
        409: (ConflictError, "Ya existe este recurso."),
        422: (ValidationError, f"Datos inválidos: {response.json().get('errors', 'Desconocido')}"),
        500: (ServerError, "Error del servidor."),
    }

    
    for codigo, (exception_class, mensaje) in error_map.items():
        if response.status_code == codigo:
            logger.error(f"Error HTTP {codigo}: {mensaje}")
            raise exception_class(mensaje)

    mensaje_fallback = f"Error inesperado: {response.status_code}"
    logger.error(mensaje_fallback)
    raise ServiceError(mensaje_fallback)
