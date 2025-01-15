import requests

class SearchGoogle:
    def __init__(self, api_key, engine_id):
        self.api_key = api_key
        self.engine_id = engine_id

    def search(self, query, start_page=1, pages=1,lang="lang_eu"):
        final_results = [] # Almacena los resultados finales
        results_per_page = 10 # Numero de resultados que muestra Google por consulta
        for page in range(pages): # Iteracion sobre el numero de paginas
            # Calculamos el resutado de comienzo de cada pagina
            start_index = (start_page - 1) * results_per_page + 1 + (page * results_per_page)
            url = f"https://www.googleapis.com/customsearch/v1?key={self.api_key}&cx={self.engine_id}&q={query}&start={start_index}&lang={lang}"
            response = requests.get(url) # Mandamos una peticion GET a la URL especificada
            # Comprobamos que la respuesta es correcta
            if response.status_code == 200: # Si el estatus es OK (200) procesamos los datos
                data = response.json() # Trabajamos con el formato JSON
                resultado = data.get("items", []) # Obtiene los resultados de la busqueda, si no hay resultados, devuelve una lista vacia
                cresults = self.custom_result(resultado) # Tratamos los datos
                final_results.extend(cresults) # Agregamos los resultados a nuesta lista previamente definida

            # Manejo de excepciones
            else:
                error_msg = f"Error al obtener la  pagina {page + 1}: HTTP {response.status_code}"
                print(error_msg)
                raise Exception(error_msg)

        # Retornamos lo almacenado en final_results
        return final_results

    def custom_result(self, results):
        custom_results = []
        # Recorremos los resultados.
        for result in results:
            # Extraemos los siguientes datos
            cresult = {
                "title": result.get("title"),
                "description": result.get("snippet"),
                "link": result.get("link")
            }
            custom_results.append(cresult) # Devuelve una lista de diccionarios con los datos relevantes de cada resultado
        return custom_results