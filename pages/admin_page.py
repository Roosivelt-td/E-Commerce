"""
Page Object para Panel de Administración
CP01: Carga masiva CSV
CP02: Edición de stock dinámico
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import os

class AdminPage(BasePage):
    # Localizadores
    INPUT_CSV = (By.ID, "csvFile")
    BTN_CARGAR_CSV = (By.XPATH, "//button[contains(text(),'Cargar')]")
    TABLA_INVENTARIO = (By.ID, "tabla-inventario")
    FILAS_PRODUCTOS = (By.CSS_SELECTOR, "#inventario-body tr")

    def __init__(self, driver):
        super().__init__(driver)

    def abrir(self):
        """Abre el panel de administración (misma URL que la tienda)"""
        self.driver.get("http://172.17.0.1:5000")
        print("✅ Panel Admin abierto")

    def cargar_csv(self, ruta_csv):
        """
        CP01: Carga masiva de productos desde CSV
        """
        if not os.path.exists(ruta_csv):
            raise Exception(f"❌ Archivo CSV no encontrado: {ruta_csv}")

        input_file = self.esperar_elemento(self.INPUT_CSV)
        input_file.send_keys(os.path.abspath(ruta_csv))

        self.click(self.BTN_CARGAR_CSV)

        # Esperar toast de confirmación
        toast = self.wait.until(EC.visibility_of_element_located((By.ID, "toast")))
        mensaje = toast.text
        print(f"✅ CSV cargado: {mensaje}")
        return mensaje

    def obtener_cantidad_productos(self):
        """Obtiene cuántos productos hay en el inventario"""
        filas = self.obtener_elementos(self.FILAS_PRODUCTOS)
        return len(filas)

    def editar_stock(self, nombre_producto, nuevo_stock):
        """Edita el stock de un producto"""
        boton_editar = (By.XPATH, f"//tr[td[text()='{nombre_producto}']]//button[contains(text(),'Editar')]")
        self.click(boton_editar)

        from selenium.webdriver.common.alert import Alert
        alert = Alert(self.driver)
        alert.send_keys(str(nuevo_stock))
        alert.accept()

        toast = self.wait.until(EC.visibility_of_element_located((By.ID, "toast")))
        mensaje = toast.text
        print(f"✅ Stock actualizado: {mensaje}")
        return mensaje

    def obtener_stock(self, nombre_producto):
        """Obtiene el stock actual de un producto"""
        celda_stock = (By.XPATH, f"//tr[td[text()='{nombre_producto}']]/td[2]")
        texto_stock = self.obtener_texto(celda_stock)
        return int(texto_stock)