import os
import re
import argparse
from transformers import GPT2Tokenizer
from openai import OpenAI
from dotenv import load_dotenv


class SmartSearch:
    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.files = self._read_files()

    def _read_files(self):
        files = {}
        for archivo in os.listdir(self.dir_path):
            file_path = os.path.join(self.dir_path, archivo)
            try:
                with open(file_path,'r', encoding='utf-8') as f:
                    files[archivo] = f.read()
            except Exception as e:
                print(f"[!] Error al leer el archivo: {file_path}")
        return files

    def regex_search(self, regex):
        coincidencias = {}
        for file, text in self.files.items():
            respuesta = ""
            while respuesta not in ('y','yes','n','no'):
                respuesta = input(f"""[-] El fichero {file} tiene una longitud de {len(text)} caracteres.
                                    Quieres procesar el fichero (yes/no): """)
            if respuesta in ('n','no'):
                continue
            matches = re.findall(regex, text, re.IGNORECASE)
            if not matches == []:
                    coincidencias[file] = matches
        return coincidencias

    def ia_search(self, prompt,model_name="gpt-4o", max_tokens=100):
        coincidencias = {}
        for file, text in self.files.items():
            respuesta = ""
            while respuesta not in ('y','yes','n','no'):
                tokens, coste = self._calcular_coste(text, prompt, model_name, max_tokens)
                while respuesta not in ('y','yes','n','no'):
                    respuesta = input(f"""El fichero {file} tiene una longitud de {tokens} caracteres (aprox. {coste})
                                        Quieres continuar? (yes/no): """)
                    if respuesta in ('n','no'):
                        continue

                    file_ssegment = self._split_file(text, model_name)

                    load_dotenv()

                    client = OpenAI()

                    resultados_segmentos = []

                    for index, segment in enumerate(file_ssegment):
                        print(f"Procesando segmento:{index + 1} {segment}")
                        chat_completion = client.chat.completions.create(
                            messages=[{
                                "role" : "user",
                                "content" : f"{prompt}\n\nTexto:\n{segment}",
                            }],
                            model=model_name,
                            max_tokens=max_tokens,
                            n=1
                        )
                        resultados_segmentos.append(chat_completion.choices[0].message.content)
                    coincidencias[file] = resultados_segmentos
                return coincidencias

    def _split_file(self, file_text, model_name):
        context_window_sizes = {
            "gpt-4": 8192,  # 8,192 tokens
            "gpt-4-32k": 32768,  # 32,768 tokens
            "gpt-3.5-turbo": 4096,  # 4,096 tokens
            "gpt-3.5-turbo-16k": 16384,  # 16,384 tokens
            "gpt-3.5-turbo-instruct": 4096,  # 4,096 tokens
            "gpt-3.5-turbo-1106": 4096,  # 4,096 tokens
            "gpt-3.5-turbo-0613": 4096,  # 4,096 tokens
            "gpt-4o": 128000,  # 128,000 tokens
            "gpt-4-1106-preview": 8192,  # 8,192 tokens
            "gpt-4-1106-vision-preview": 8192  # 8,192 tokens
        }
        return [file_text[i:i+context_window_sizes[model_name]]
                for i in range(0, len(file_text), context_window_sizes[model_name])]

    def _calcular_coste(self, text, prompt, model_name, max_tokens):
        precios = {
            "gpt-4": {"input_cost": 0.03, "output_cost": 0.06},
            "gpt-4-32k": {"input_cost": 0.06, "output_cost": 0.12},
            "gpt-3.5-turbo": {"input_cost": 0.0015, "output_cost": 0.002},
            "gpt-3.5-turbo-16k": {"input_cost": 0.003, "output_cost": 0.004},
            "gpt-3.5-turbo-instruct": {"input_cost": 0.0015, "output_cost": 0.002},
            "gpt-3.5-turbo-1106": {"input_cost": 0.001, "output_cost": 0.002},
            "gpt-3.5-turbo-0613": {"input_cost": 0.0015, "output_cost": 0.002},
            "gpt-4o": {"input_cost": 0.01, "output_cost": 0.03},
            "gpt-4-1106-preview": {"input_cost": 0.01, "output_cost": 0.03},
            "gpt-4-1106-vision-preview": {"input_cost": 0.01, "output_cost": 0.03}
        }

        tokenizar = GPT2Tokenizer.from_pretrained("gpt2")
        len_tokens_prompt = len(tokenizar.tokenize(prompt))
        len_tokens_text = len(tokenizar.tokenize(text))

        input_cost = ((len_tokens_prompt + len_tokens_text) / 1000) * precios[model_name]["input_cost"]
        output_cost = (max_tokens / 1000) * precios[model_name]["output_cost"]

        return (len_tokens_prompt + len_tokens_text, input_cost + output_cost)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Realiza busquedas con expresiones regulares.')
    parser.add_argument('-d', '--dir-path',type=str, help='Ruta del directorio donde se encuentran los archivos.')
    parser.add_argument("-r", "--regex",type=str, help="Expresion regular que quieres buscar.")
    parser.add_argument("-p","--prompt",type=str, help="Prompt que quieres buscar.")
    parser.add_argument("-m", "--model-name", type=str,default="gpt-3.5-turbo-1106", help="Nombre del modelo de IA.")
    parser.add_argument("-mt","--max-tokens",type=int,default=1000,help="Max tokens que quiere buscar.")

    args = parser.parse_args()

    if args.regex:
        search = SmartSearch(args.dir_path)
        resultados = search.regex_search(args.regex)
        for file, results in resultados.items():
            print(f"{file}: {results}")
            print()

    if args.prompt:
        search = SmartSearch(args.dir_path)
        resultados = search.ia_search(args.prompt, args.model_name, args.max_tokens)
        for file, results in resultados.items():
            print(f"{file}: {results}")
            print()
