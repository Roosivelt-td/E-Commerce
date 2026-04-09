"""
Pruebas de Gestión de Inventario
CP01: Carga masiva de productos CSV
CP02: Edición de stock dinámico
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.admin_page import AdminPage
import os

class TestInventario:

    @pytest.fixture(params=["firefox", "chrome"])
    def driver(self, request):
        """Fixture para pruebas en múltiples navegadores"""
        if request.param == "firefox":
            driver = webdriver.Firefox()
        elif request.param == "chrome":
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        else:
            pytest.skip(f"Navegador {request.param} no soportado")

        driver.maximize_window()
        yield driver
        driver.quit()

    def test_cp01_carga_masiva_csv(self, driver):
        """CP01: Carga masiva de productos CSV"""
        print("\n" + "="*60)
        print("CP01 - CARGA MASIVA DE PRODUCTOS CSV")
        print(f"🌐 Navegador: {driver.name}")
        print("="*60)

        admin = AdminPage(driver)
        admin.abrir()

        productos_antes = admin.obtener_cantidad_productos()
        print(f"📊 Productos antes: {productos_antes}")

        ruta_csv = os.path.abspath("data/productos.csv")
        admin.cargar_csv(ruta_csv)

        productos_despues = admin.obtener_cantidad_productos()
        print(f"📊 Productos después: {productos_despues}")

        assert productos_despues > productos_antes
        print(f"✅ CP01 exitoso: Se agregaron {productos_despues - productos_antes} productos")

    def test_cp02_edicion_stock_dinamico(self, driver):
        """CP02: Edición de stock dinámico"""
        print("\n" + "="*60)
        print("CP02 - EDICIÓN DE STOCK DINÁMICO")
        print(f"🌐 Navegador: {driver.name}")
        print("="*60)

        admin = AdminPage(driver)
        admin.abrir()

        producto = "Laptop Gamer"
        stock_inicial = admin.obtener_stock(producto)
        print(f"📊 Stock inicial de {producto}: {stock_inicial}")

        nuevo_stock = 10
        mensaje_toast = admin.editar_stock(producto, nuevo_stock)
        print(f"📢 Toast: {mensaje_toast}")

        assert "actualizado" in mensaje_toast.lower()

        stock_final = admin.obtener_stock(producto)
        assert stock_final == nuevo_stock

        print(f"✅ CP02 exitoso: Stock actualizado de {stock_inicial} a {stock_final}")