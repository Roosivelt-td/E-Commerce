"""
Pruebas de Validación Real-Time
CP03: Flujo de compra completo
CP04: Persistencia de sesión
CP05: Prueba de concurrencia
"""

import pytest
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.admin_page import AdminPage
from pages.store_page import StorePage
#BASE_URL = "http://localhost:5000"
BASE_URL = "http://172.17.0.1:5000"

class TestEcommerce:

    @pytest.fixture(params=["firefox", "chrome"])
    def driver(self, request):

        if request.param == "firefox":
            options = webdriver.FirefoxOptions()
        else:
            options = webdriver.ChromeOptions()

        driver = webdriver.Remote(
            command_executor="http://localhost:4444",
            options=options
        )

        driver.maximize_window()
        yield driver
        driver.quit()
#--------------------------
        # """Fixture para pruebas en múltiples navegadores"""
        # if request.param == "firefox":
        #     driver = webdriver.Firefox()
        # elif request.param == "chrome":
        #     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        # else:
        #     pytest.skip(f"Navegador {request.param} no soportado")
        #
        # driver.maximize_window()
        # yield driver
        # driver.quit()

    def test_cp03_flujo_compra_completo(self, driver):
        """CP03: Flujo de compra completo E2E"""
        print("\n" + "="*60)
        print("CP03 - FLUJO DE COMPRA COMPLETO E2E")
        print(f"🌐 Navegador: {driver.name}")
        print("="*60)

        producto = "Mouse Inalámbrico"
        wait = WebDriverWait(driver, 10)

        #driver.get("http://localhost:5000")
        driver.get(BASE_URL)
        # Stock inicial
        stock_celda = wait.until(EC.presence_of_element_located(
            (By.XPATH, f"//tr[td[text()='{producto}']]/td[2]")
        ))
        stock_inicial = int(stock_celda.text)
        print(f"📊 Stock inicial de {producto}: {stock_inicial}")

        # Comprar
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")

        btn_comprar = wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//div[contains(@class,'producto')][.//h3[text()='{producto}']]//button[contains(@class,'btn-comprar')]")
        ))
        btn_comprar.click()
        print(f"🛒 Click en comprar - {producto}")

        # Toast
        toast = wait.until(EC.visibility_of_element_located((By.ID, "toast")))
        print(f"📢 Toast: {toast.text}")

        # Volver y verificar
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)

        stock_celda_actualizada = driver.find_element(
            By.XPATH, f"//tr[td[text()='{producto}']]/td[2]"
        )
        stock_final = int(stock_celda_actualizada.text)
        print(f"📊 Stock final de {producto}: {stock_final}")

        assert stock_final == stock_inicial - 1

        print(f"✅ CP03 exitoso: Stock disminuyó de {stock_inicial} a {stock_final}")

    def test_cp04_persistencia_sesion(self, driver):
        """CP04: Persistencia de sesión"""
        print("\n" + "="*60)
        print("CP04 - PERSISTENCIA DE SESIÓN")
        print(f"🌐 Navegador: {driver.name}")
        print("="*60)

        driver.get(BASE_URL)

        session_id_inicial = driver.execute_script("return localStorage.getItem('sessionId');")
        print(f"🔑 Session ID inicial: {session_id_inicial}")

        driver.execute_script("localStorage.setItem('carrito', JSON.stringify([{id:1, nombre:'Laptop', cantidad:1}]));")
        driver.refresh()
        time.sleep(1)

        session_id_final = driver.execute_script("return localStorage.getItem('sessionId');")
        carrito = driver.execute_script("return localStorage.getItem('carrito');")

        assert session_id_inicial == session_id_final
        assert carrito is not None

        print(f"✅ CP04 exitoso: Sesión persistió correctamente")

    def test_cp05_prueba_concurrencia(self, driver):
        """CP05: Prueba de Concurrencia"""
        print("\n" + "="*60)
        print("CP05 - PRUEBA DE CONCURRENCIA")
        print(f"🌐 Navegador: {driver.name}")
        print("="*60)

        # Preparar stock = 1
        admin = AdminPage(driver)
        admin.abrir()
        producto = "Teclado Mecánico"
        admin.editar_stock(producto, 1)
        print(f"📊 Stock de {producto} puesto a 1 unidad")

        driver.get("about:blank")

        resultados = {"exitosos": 0, "fallos": 0}
        lock = threading.Lock()

        def comprar_usuario(usuario_id, producto):

            driver_local = None

            try:

                if usuario_id == 1:
                    options = webdriver.FirefoxOptions()
                else:
                    options = webdriver.ChromeOptions()

                driver_local = webdriver.Remote(
                    command_executor="http://localhost:4444",
                    options=options
                )

                driver_local.maximize_window()
                driver_local.get(BASE_URL)

                btn = WebDriverWait(driver_local, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH,
                         f"//div[contains(@class,'producto')][.//h3[text()='{producto}']]//button[contains(@class,'btn-comprar')]")
                    )
                )

                btn.click()

                with lock:
                    resultados["exitosos"] += 1

                print(f"👤 Usuario {usuario_id}: ✅ Compra exitosa")

            except Exception as e:

                with lock:
                    resultados["fallos"] += 1

                print(f"👤 Usuario {usuario_id}: ❌ Compra fallida")

            finally:

                if driver_local:
                    driver_local.quit()

        print("\n🚀 Iniciando compras simultáneas...")
        hilo1 = threading.Thread(target=comprar_usuario, args=(1, producto))
        hilo2 = threading.Thread(target=comprar_usuario, args=(2, producto))

        hilo1.start()
        hilo2.start()
        hilo1.join()
        hilo2.join()

        print(f"\n📊 Resultados: {resultados['exitosos']} exitosos, {resultados['fallos']} fallos")

        print("\n📝 NOTA: En backend real con transacciones atómicas, solo uno tendría éxito.")

        assert resultados["exitosos"] >= 1
        print(f"\n✅ CP05 - Prueba de concurrencia completada")