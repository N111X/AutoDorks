import os
import requests


class Downloader:
    def __init__(self, directorio_destino):
        self.directorio = directorio_destino
        self.crear_directorio()

    def crear_directorio(self):
        if not os.path.exists(self.directorio):
            os.makedirs(self.directorio)

    def download_archivos(self, url):
        try:
            response = requests.get(url)
            nombre_archivo = url.split("/")[-1]
            ruta_completa = os.path.join(self.directorio, nombre_archivo)
            with open(ruta_completa, "wb") as archivo:
                archivo.write(response.content)
            print(f"Archivo descargado con éxito: {nombre_archivo} en {ruta_completa}.")
        except Exception as e:
            print(f"Error al descargar archivos en el directorio {self.directorio}: {e}")

    def filtrar_archivos(self, urls, tipos_archivos=["all"]):
        if tipos_archivos == ["all"]:
            for url in urls:
                self.download_archivos(url)
        else:
            for url in urls:
                if any(url.endswith(f"{tipo}") for tipo in tipos_archivos):
                    self.download_archivos(url)