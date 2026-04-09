# Proyecto de Pruebas Automatizadas E‑Commerce

## Descripción

Este proyecto implementa pruebas automatizadas para una aplicación web de comercio electrónico utilizando **Python, Pytest, Selenium y Selenium Grid con Docker**. El objetivo es validar funcionalidades críticas del sistema como flujo de compra, persistencia de sesión y concurrencia de usuarios.

---

# Tecnologías Utilizadas

* Python 3.12
* Pytest
* Selenium WebDriver
* Selenium Grid
* Docker
* Docker Compose

---

# Estructura del Proyecto

```
E-Commerce/
│
├── pages/
│   ├── base_page.py
│   ├── admin_page.py
│   └── store_page.py
│
├── tests/
│   ├── test_ecommerce.py
│   └── test_inventario.py
│
├── reports/
│   └── reporte.html
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## ⚖️  Reglas de Oro Implementadas
1.  **Stock Cero:** Si un producto llega a stock 0, el botón "Añadir al carrito" cambia automáticamente a "Sin Stock" y se deshabilita.
2.  **Cero time.sleep():** Toda sincronización se maneja mediante `WebDriverWait` y `ExpectedConditions`.
3.  **Patrón POM:** Separación estricta entre la lógica de la página y la lógica de las pruebas.

## 🧪 Casos de Prueba Principales
- **CP01 - Carga Masiva:** Validación de inventario mediante carga de archivos CSV.
- **CP02 - Edición Dinámica:** Actualización de stock y validación de alertas Toast.
- **CP03 - End-to-End:** Flujo completo de compra con decremento automático de stock.
- **CP04 - Persistencia:** Verificación de carrito de compras entre diferentes sesiones/navegadores.
- **CP05 - Concurrencia:** Prueba de carrera crítica (Race Condition) donde dos hilos intentan comprar la última unidad disponible.

## 🚀 Instrucciones de Ejecución

### 1. Requisitos Previos
- Docker y Docker Compose.
- Python 3.10+.
# Instalación del Proyecto

## 1. Clonar el repositorio

```bash
git clone https://github.com/Roosivelt-td/E-Commerce
cd E-Commerce
```

## 2. Crear entorno virtual

```bash
python -m venv .venv 
python3 -m venv .venv #si no funciona con python -m venv .venv  
source .venv/bin/activate
```

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# Ejecución del Servidor

Ejecutar el proyecto web:

```
python servidor.py
```
El proyecto web debe ejecutarse en el puerto:

```
http://localhost:5000
```

Ejemplo si es Flask:

```bash
python app.py
```

---

# Configuración de Selenium Grid con Docker
## Iniciar contenedores
#### Abrir otro terminal y ejecutar
Verificar instalación de DOCKER para instalarlo 
```bash
docker --version
```

```bash
docker compose up -d
```
 ó con esto
```bash
docker-compose up
```
si no funciona: implementar --> sudo
## Verificar contenedores

```bash
docker ps
```

Deberías ver:

* selenium-hub
* chrome
* firefox

---

# Interfaz de Selenium Grid

Panel de administración:

```
http://localhost:4444/ui
```

Aquí puedes ver:

* nodos activos
* sesiones de navegador
* estado del grid

---

# Configuración de URL para Docker

Cuando Selenium se ejecuta dentro de Docker no puede acceder a `localhost` de tu máquina.

Por esta razón se utiliza la IP del host:

```
http://172.17.0.1:5000
```

Esto permite que los navegadores dentro de Docker accedan al servidor que corre en tu computadora.

---

# Casos de Prueba Implementados

## CP01 – Carga masiva de productos

Valida que el sistema pueda cargar múltiples productos desde un archivo CSV.

Validaciones:

* archivo cargado correctamente
* productos insertados en la tabla

---

## CP02 – Edición dinámica de stock

Permite modificar el stock de un producto desde el panel de administración.

Validaciones:

* apertura del cuadro de edición
* actualización del stock
* confirmación mediante mensaje (toast)

---

## CP03 – Flujo de compra completo

Simula el proceso de compra de un producto desde la tienda.

Pasos:

1. Obtener stock inicial
2. Hacer clic en comprar
3. Verificar mensaje de confirmación
4. Validar que el stock disminuya

---

## CP04 – Persistencia de sesión

Valida que la sesión del usuario se mantenga después de refrescar la página.

Validaciones:

* sessionId en localStorage
* persistencia del carrito

---

## CP05 – Prueba de concurrencia

Simula múltiples usuarios comprando el mismo producto al mismo tiempo.

Objetivo:

* detectar problemas de concurrencia
* validar consistencia del inventario

---

# Ejecución de Pruebas

Ejecutar en otra terminal:

```bash
source .venv/bin/activate
```
Ejecutar todas las pruebas:

```bash
pytest -v
```

Ejecutar con reporte HTML:

```bash
pytest --html=reports/reporte.html
```

---

# Reportes de Prueba

Los reportes se generan en:

```
reports/reporte.html
```

Incluyen:

* resultados de pruebas
* tiempo de ejecución
* estado (passed / failed)

---

# Ejecución en Paralelo (Opcional)

Instalar plugin:

```bash
pip install pytest-xdist
```
Ejecutar una sola prueba específica 
```bash
pytest tests/test_ecommerce.py::TestEcommerce::test_cp03_flujo_compra_completo -v
```

Ejecutar pruebas en paralelo:

```bash
pytest -n 4
```

Ejecución en Paralelo (2 hilos):
```bash
pytest -n 2 tests/
```

Generar Reporte HTML:
```bash
pytest --html=reports/reporte_final.html --self-contained-html
```
---

# Buenas Prácticas Implementadas

* Page Object Model (POM)
* Pruebas parametrizadas
* Automatización multi‑navegador
* Uso de Docker para entornos reproducibles

---

# Conclusión

Este proyecto demuestra la implementación de un sistema de pruebas automatizadas moderno utilizando Selenium Grid y Docker. Permite ejecutar pruebas en múltiples navegadores de forma escalable y reproducible.


## 📊 Reportabilidad
El framework genera reportes detallados en la carpeta `reports/`. En caso de fallo, se adjunta automáticamente una captura de pantalla (`screenshot`) al reporte HTML para facilitar el análisis de errores.

---
**Docente:** Mg. Hinostroza Farfán, Hugo  
**Fecha:** Abril 2026 | Semana-10  
**Sección:** 7 A/B


