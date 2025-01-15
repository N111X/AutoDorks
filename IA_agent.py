from gpt4all import GPT4All
from openai import OpenAI

class IAGeneratorInterface:
    def generate(self, prompt):
        raise NotImplementedError("Este método debe ser implementado por la subclase.")

class GPT4ALLGENERATOR(IAGeneratorInterface):
    def __init__(self, model_name='orca-mini-3b-gguf2-q4_0.gguf'):
        self.model = GPT4All(model_name)

    def generate(self, prompt):
        return self.model.generate(prompt)

class OpenAIGenerator(IAGeneratorInterface):
    def __init__(self,model_name="gpt-4o"):
        self.model_name = model_name
        self.client = OpenAI()

    def generate(self, prompt):
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=self.model_name,
        )
        return chat_completion.choices[0].message.content

class IAagent:

    def __init__(self, generator):
        self.generator = generator

    def generate_gdork(self, description):

        prompt = self._build_prompt(description)
        try:
            output = self.generator.generate(prompt)
            return output.strip()
        except Exception as e:
            print(f'Error al generar el Google Dork: {e}')
            return None

    def _build_prompt(self, description):

        return f"""
Genera un Google Dork específico basado en la descripción del usuario. Un Google Dork utiliza operadores avanzados en motores de búsqueda para encontrar información específica difícil de encontrar mediante una búsqueda normal. Convierte la descripción del usuario en un Google Dork preciso. Algunos ejemplos:

Descripción: Documentos PDF relacionados con la seguridad informática publicados en el último año.
Google Dork: filetype:pdf "seguridad informática" after:2023-01-01

Descripción: Presentaciones de PowerPoint sobre cambio climático disponibles en sitios .edu.
Google Dork: site:.edu filetype:ppt "cambio climático"

Descripción: Listas de correos electrónicos en archivos de texto dentro de dominios gubernamentales.
Google Dork: site:.gov filetype:txt "email" | "correo electrónico"

Ahora, genera el Google Dork para esta descripción:
Descripción: {description}"""





