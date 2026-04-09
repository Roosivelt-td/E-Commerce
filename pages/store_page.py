"""
Page Object para la Tienda (Storefront)
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class StorePage(BasePage):
    # Localizadores
    PRODUCTOS = (By.CSS_SELECTOR, ".producto")
    BTN_COMPRAR = (By.CSS_SELECTOR, ".btn-comprar")
    BTN_SIN_STOCK = (By.CSS_SELECTOR, ".btn-sin-stock")

    def __init__(self, driver):
        super().__init__(driver)

    def abrir(self):
        """Abre la tienda"""
        self.driver.get("http://localhost:5000")
        print("✅ Tienda abierta")

    def obtener_productos(self):
        """Obtiene la lista de productos visibles"""
        return self.obtener_elementos(self.PRODUCTOS)

    def comprar_producto(self, nombre_producto):
        """Compra un producto específico por su nombre"""
        boton = (By.XPATH, f"//div[contains(@class,'producto')][.//h3[text()='{nombre_producto}']]//button[contains(@class,'btn-comprar')]")

        elemento = self.esperar_elemento(boton)
        if "btn-sin-stock" in elemento.get_attribute("class"):
            raise Exception(f"❌ {nombre_producto} está sin stock - No se puede comprar")

        self.click(boton)
        print(f"✅ Comprado: {nombre_producto}")

        toast = self.wait.until(EC.visibility_of_element_located((By.ID, "toast")))
        return toast.text

    def verificar_boton_sin_stock(self, nombre_producto):
        """Verifica que producto con stock 0 tenga botón 'Sin Stock' deshabilitado"""
        boton = (By.XPATH, f"//div[contains(@class,'producto')][.//h3[text()='{nombre_producto}']]//button")
        elemento = self.esperar_elemento(boton)

        esta_deshabilitado = elemento.get_attribute("disabled") is not None
        if esta_deshabilitado:
            print(f"✅ Regla de Oro #1: '{nombre_producto}' tiene botón 'Sin Stock'")
        else:
            raise Exception(f"❌ Regla de Oro #1 violada: '{nombre_producto}' tiene stock 0 pero botón habilitado")

        return esta_deshabilitado