
from typing import Callable, Dict, Any, Tuple


class SagaAction:
    

    def __init__(
        self,
        execute_fn: Callable[[Dict[str, Any]], Tuple[str, Dict[str, Any]]],
        compensate_fn: Callable[[str], bool],
    ):
      
        self.execute_fn = execute_fn
        self.compensate_fn = compensate_fn
        self.url: str = None

    def ejecutar(self, data: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
       
        url, response_data = self.execute_fn(data)
        self.url = url
        return url, response_data

    def compensar(self, id_recurso: str) -> bool:
       
        return self.compensate_fn(id_recurso)
