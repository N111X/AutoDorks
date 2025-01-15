import os
import sys
import argparse
from search import SearchGoogle
from results_parser import ResultsParser
from file_downloader import Downloader
from IA_agent import OpenAIGenerator, GPT4ALLGENERATOR, IAagent
from dotenv import load_dotenv
from browserautosearch import BrowserAutoSearch
from config import openai_configure, load_env, env_configure


def configure_ia(autoDork):
    """
    Configura el generador de Dorks utilizando IA segun la eleccion del usuario.
    """
    respuesta = input("Quieres utilizar GPT4 de OpenAI para generar un Dork (yes/no): ").lower()

    if respuesta in ("yes", "y"):
        load_dotenv()
        if not "OPENAI_API_KEY" in os.environ:
            openai_configure()
            load_dotenv()
        openai_generator = OpenAIGenerator()
        ia_agent = IAagent(openai_generator)
    else:
        print("Utilizando GPT4ALL y ejecutando la generacion en local. Puede tardar varios minutos")
        gpt4all_generator = GPT4ALLGENERATOR()
        ia_agent = IAagent(gpt4all_generator)

    return ia_agent.generate_gdork(autoDork)


def process_search_results(query, selenium_, start_page, page, lang, configure_env):
    """
    Procesa los resultados de busqueda segun la opcion seleccionada (Selenium o Google API).
    """
    if selenium_:
        browser = BrowserAutoSearch()
        browser.search_in_google(search_term=query)
        results = browser.google_results_parser()
        browser.quit()
    else:
        API_KEY_GOOGLE, SEARCH_ENGINE_ID = load_env(configure_env=configure_env)
        gsearch = SearchGoogle(API_KEY_GOOGLE, SEARCH_ENGINE_ID)
        results = gsearch.search(query, start_page=start_page, pages=page, lang=lang)

    return results


def handle_output(results, output_JSON, output_HTML, download, file_types):
    """
    Maneja la exportacion de resultados y la descarga de archivos.
    """
    rparser = ResultsParser(results)
    rparser.mostrar_resultado()

    if output_JSON:
        rparser.exportar_JSON(output_JSON)

    if output_HTML:
        rparser.exportar_HTML(output_HTML)

    if download:
        url = [resultado["link"] for resultado in results]
        fdownloader = Downloader("Descargas")
        fdownloader.filtrar_archivos(url, file_types)


def main(query, configure_env, start_page, page, lang, output_JSON, output_HTML, download, autoDork, selenium_):
    if configure_env:
        load_env(configure_env=True)

    API_KEY_GOOGLE, SEARCH_ENGINE_ID = load_env(configure_env=configure_env)

    if autoDork:
        dork = configure_ia(autoDork)
        print(f"Dork generado: {dork}")
        sys.exit(1)

    if not query:
        print("Error: Debes proporcionar un Dork con -q o generar uno con -gd.")
        sys.exit(1)

    results = process_search_results(query, selenium_, start_page, page, lang, configure_env)
    handle_output(results, output_JSON, output_HTML, download, file_types=download.split(",") if download else [])


if __name__ == "__main__":
    # Configuracion de los argumentos
    parser = argparse.ArgumentParser(
        description='Desarrollado por: N111X\nHerramienta avanzada para realizar Dorking y automatizacion de busquedas.',
        add_help=True)

    parser.add_argument("-q", "--query", type=str,
                        help="Especifica el Dork a realizar. Ejemplo: 'intitle:\"index of\" filetype:sql'")

    parser.add_argument("-c", "--configure", action="store_true",
                        help="Configura el archivo .env para definir tus claves API y ID de motor de busqueda.")

    parser.add_argument("-sp", "--start-page", type=int, default=1,
                        help="Pagina de inicio para obtener los resultados (default: 1).")

    parser.add_argument("-p", "--pages", type=int, default=1,
                        help="Numero de paginas de resultados a obtener (default: 1).")

    parser.add_argument("-l", "--language", type=str, default="lang_es",
                        help="Idioma de los resultados (default: lang_es).")

    parser.add_argument("-j", "--json", type=str, help="Especifica el archivo de salida en formato JSON.")

    parser.add_argument("-html", "--html", type=str, help="Especifica el archivo de salida en formato HTML.")

    parser.add_argument("-d", "--download", type=str, default=None,
                        help="Especifica los tipos de archivos a descargar (ejemplo: pdf, zip, sql).")

    parser.add_argument("-gd", "--generate-dork", type=str,
                        help="Genera un Dork automaticamente usando IA. Ejemplo: 'dork para contrasenas en texto plano'.")

    parser.add_argument("-s", "--selenium", action="store_true", default=False,
                        help="Activa Selenium para realizar busquedas automatizadas en el navegador.")

    args = parser.parse_args()

    main(query=args.query,
         configure_env=args.configure,
         page=args.pages,
         start_page=args.start_page,
         lang=args.language,
         output_JSON=args.json,
         output_HTML=args.html,
         download=args.download,
         autoDork=args.generate_dork,
         selenium_=args.selenium)