from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time

class BrowserAutoSearch:
    def __init__(self, browser_type="chrome"):
        """
        Inicializa el navegador segun el tipo especificado (chrome o firefox).
        """
        self.browser = self._initialize_browser(browser_type)

    def _initialize_browser(self, browser_type):
        """
        Configura e inicializa el navegador.
        """
        browsers = {
            "firefox": {
                "manager": GeckoDriverManager,
                "service": FirefoxService,
                "options": webdriver.FirefoxOptions(),
                "driver": webdriver.Firefox
            },
            "chrome": {
                "manager": ChromeDriverManager,
                "service": ChromeService,
                "options": webdriver.ChromeOptions(),
                "driver": webdriver.Chrome
            }
        }

        if browser_type not in browsers:
            raise ValueError("[!] Navegador no soportado. Usa 'chrome' o 'firefox'.")

        browser_info = browsers[browser_type]
        try:
            return browser_info["driver"](
                service=browser_info["service"](browser_info["manager"]().install()),
                options=browser_info["options"]
            )
        except Exception as e:
            print(f"Error al iniciar el navegador {browser_type}: {e}")
            raise

    def search_in_google(self, search_term):
        """
        Realiza una busqueda en Google con el termino especificado.
        """
        self.browser.get("http://www.google.com")
        search_box = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, 'q'))
        )
        search_box.send_keys(search_term, Keys.ENTER)

    def google_results_parser(self):
        """
        Extrae resultados de busqueda de Google.
        """
        try:
            results = WebDriverWait(self.browser, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.g'))
            )
        except Exception as e:
            print(f"[!] Error al obtener los resultados: {e}")
            return []

        custom_results = []
        for result in results:
            try:
                title = result.find_element(By.CSS_SELECTOR, 'h3').text
                link = result.find_element(By.TAG_NAME, 'a').get_attribute('href')
                description = result.find_element(By.CSS_SELECTOR, 'div.VwiC3b').text
                custom_results.append({"title": title, "link": link, "description": description})
            except Exception as e:
                print(f"[!] No se pudo extraer un elemento: {e}")
                continue
        return custom_results

    def quit(self):
        """
        Cierra el navegador.
        """
        try:
            self.browser.quit()
        except Exception as e:
            print(f"[!] Error al cerrar el navegador: {e}")