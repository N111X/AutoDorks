import json
from rich.console import Console
from rich.table import Table
from rich.box import ROUNDED

class ResultsParser:
    def __init__(self, resultados):
        self.resultados = resultados

    def exportar_HTML(self, ruta_HTML):
        with open("template.html", "r", encoding="utf-8") as template:
            plantilla = template.read()

        elementos_HTML = ''
        for indice, resultado in enumerate(self.resultados, start=1):
            elemento = f'<div class="resultados">' \
                       f'<div class="indice">Resultado {indice}</div>' \
                       f'<h5>{resultado["title"]}</h5>' \
                       f'<p>{resultado["description"]}</p>' \
                       f'<a href="{resultado["link"]}" target="_blank">{resultado["link"]}</a>' \
                       f'</div>'
            elementos_HTML += elemento

        informe = plantilla.replace('{{ resultados }}', elementos_HTML)
        with open(ruta_HTML, "w", encoding="utf-8") as plantilla:
            plantilla.write(informe)
        print(f"Resultados exportados en HTML:\nFichero creado en {ruta_HTML}")

    def exportar_JSON(self, ruta_JSON):
        with open(ruta_JSON, "w", encoding="utf-8") as plantilla_JSON:
            json.dump(self.resultados, plantilla_JSON, ensure_ascii=False, indent=4)
        print(f"Resultados exportados en JSON.\nFichero creado en {ruta_JSON}")

    def mostrar_resultado(self):
        console = Console()

        # Crear la tabla con un estilo atractivo
        table = Table(show_header=True, header_style="bold bright_blue", box=ROUNDED, show_lines=True)

        # Definir los estilos de las columnas
        table.add_column("#", style="bold bright_red on white", justify="center",
                         no_wrap=True)  # Fondo amarillo y texto rojo brillante
        table.add_column("Titulo", style="bold bright_cyan", justify="left")  # Subrayado y cian brillante
        table.add_column("Descripcion", style="italic white on black",
                         justify="left")  # Blanco sobre negro y en itálico
        table.add_column("Link", style="bold bright_green on black", justify="center",
                         no_wrap=True)  # Verde brillante sobre negro

        # Añadir filas a la tabla
        for indice, resultado in enumerate(self.resultados, start=1):
            table.add_row(str(indice), resultado["title"], resultado["description"], resultado["link"])

        # Mostrar la tabla
        console.print(table)