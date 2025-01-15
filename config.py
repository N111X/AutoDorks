# config.py

import os
import sys
from dotenv import load_dotenv, set_key


def env_configure():
    """
    Solicita al usuario las claves API necesarias y las guarda en el archivo .env.
    """
    api_key = input("[?] Introduce el API key: ")
    engine_id = input("[?] Introduce el engine id: ")
    set_key(".env", "API_KEY_GOOGLE", api_key)
    set_key(".env", "SEARCH_ENGINE_ID", engine_id)
    print("[-] Archivo .env configurado correctamente")


def openai_configure():
    """
    Solicita al usuario la clave API de OpenAI y la guarda en el archivo .env.
    """
    api_key = input("[?] Introduce el API key de OpenAI: ")
    set_key(".env", "OPENAI_API_KEY", api_key)
    print("[-] Archivo .env configurado satisfactoriamente.")


def load_env(configure_env=False):
    """
    Carga las variables de entorno desde el archivo .env. Si el archivo no existe o se requiere
    configuración, solicita las claves necesarias y termina el programa si es necesario.

    :param configure_env: Si es True, configura el archivo .env antes de cargar las variables.
    :return: Una tupla con las claves API de Google y el ID del motor de búsqueda.
    """
    if configure_env or not os.path.exists(".env"):
        env_configure()
        sys.exit(1)

    load_dotenv()

    API_KEY_GOOGLE = os.getenv("API_KEY_GOOGLE")
    SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")
    return (API_KEY_GOOGLE, SEARCH_ENGINE_ID)
