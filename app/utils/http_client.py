

import os
from typing import Dict, Any, Optional
import requests
from requests import Response

from app.utils.logger_config import setup_logger


logger = setup_logger(__name__)


class HttpClient:
   

    @staticmethod
    def _should_verify_ssl() -> bool:
        
        flask_env = os.getenv("FLASK_ENV", "development").lower()
        return flask_env == "production"

    @classmethod
    def get(
        cls,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 10,
    ) -> Response:
      
        logger.debug(f"Petición GET a: {url}")
        return requests.get(
            url,
            headers=headers,
            timeout=timeout,
            verify=cls._should_verify_ssl(),
        )

    @classmethod
    def post(
        cls,
        url: str,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 10,
    ) -> Response:
       
        logger.debug(f"Petición POST a: {url}")
        return requests.post(
            url,
            json=json,
            headers=headers,
            timeout=timeout,
            verify=cls._should_verify_ssl(),
        )

    @classmethod
    def put(
        cls,
        url: str,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 10,
    ) -> Response:
        
        logger.debug(f"Petición PUT a: {url}")
        return requests.put(
            url,
            json=json,
            headers=headers,
            timeout=timeout,
            verify=cls._should_verify_ssl(),
        )

    @classmethod
    def delete(
        cls,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 10,
    ) -> Response:
        logger.debug(f"Petición DELETE a: {url}")
        return requests.delete(
            url,
            headers=headers,
            timeout=timeout,
            verify=cls._should_verify_ssl(),
        )
