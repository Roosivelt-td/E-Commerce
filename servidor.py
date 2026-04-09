"""
Servidor simple para el E-Commerce Real-Time
Ejecutar: python servidor.py
"""

from flask import Flask, send_from_directory
import os

app = Flask(__name__)

# Directorio donde está el index.html
ECOMMERCE_DIR = os.path.join(os.path.dirname(__file__), "ecommerce_app")

@app.route('/')
def index():
    return send_from_directory(ECOMMERCE_DIR, 'index.html')

@app.route('/<path:path>')
def archivos(path):
    return send_from_directory(ECOMMERCE_DIR, path)

if __name__ == '__main__':
    print("="*60)
    print("🛒 E-COMMERCE REAL-TIME INICIADO")
    print("="*60)
    print("📱 Tienda y Admin disponibles en: http://localhost:5000")
    print("⚠️  Los cambios en Admin se reflejan automáticamente en Tienda")
    print("="*60)
    print("Presiona Ctrl+C para detener el servidor")
    print("="*60)
    app.run(debug=True, port=5000, host='0.0.0.0')