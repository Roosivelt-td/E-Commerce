"""
Clase Base con WebDriverWait - PROHIBIDO time.sleep()
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
from datetime import datetime

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # Espera máxima 10 segundos
        self.wait_corto = WebDriverWait(driver, 3)  # Para alertas

    def click(self, locator):
        """Espera a que el elemento sea clickeable y hace clic"""
        elemento = self.wait.until(EC.element_to_be_clickable(locator))
        elemento.click()
        return True

    def escribir(self, locator, texto):
        """Espera y escribe texto en un campo"""
        elemento = self.wait.until(EC.visibility_of_element_located(locator))
        elemento.clear()
        elemento.send_keys(texto)

    def obtener_texto(self, locator):
        """Obtiene el texto de un elemento"""
        elemento = self.wait.until(EC.presence_of_element_located(locator))
        return elemento.text

    def esperar_elemento(self, locator):
        """Espera que un elemento esté visible"""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def esperar_desaparezca(self, locator):
        """Espera que un elemento desaparezca"""
        return self.wait.until(EC.invisibility_of_element_located(locator))

    def obtener_elementos(self, locator):
        """Obtiene múltiples elementos"""
        return self.driver.find_elements(*locator)

    def capturar_pantalla(self, nombre):
        """Toma captura de pantalla para reportes"""
        os.makedirs("reports/screenshots", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta = f"reports/screenshots/{nombre}_{timestamp}.png"
        self.driver.save_screenshot(ruta)
        return ruta