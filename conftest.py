# conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

GRID_URL = "http://localhost:4444"

@pytest.fixture(params=["firefox", "edge"])
def driver_grid(request):
    """Fixture para ejecutar pruebas en Selenium Grid"""

    if request.param == "firefox":
        options = webdriver.FirefoxOptions()
        driver = RemoteWebDriver(command_executor=GRID_URL, options=options)
    elif request.param == "edge":
        options = webdriver.EdgeOptions()
        driver = RemoteWebDriver(command_executor=GRID_URL, options=options)
    else:
        pytest.skip(f"Navegador {request.param} no soportado")

    driver.maximize_window()
    yield driver
    driver.quit()

# Para pruebas que necesitan navegador específico
@pytest.fixture
def driver_firefox_grid():
    options = webdriver.FirefoxOptions()
    driver = RemoteWebDriver(command_executor=GRID_URL, options=options)
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture
def driver_edge_grid():
    options = webdriver.EdgeOptions()
    driver = RemoteWebDriver(command_executor=GRID_URL, options=options)
    driver.maximize_window()
    yield driver
    driver.quit()