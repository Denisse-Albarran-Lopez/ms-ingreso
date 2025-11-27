import requests
import json

BASE_URL = "http://localhost:8000"

def test_register_unam():
    data = {
        "correo": "test@comunidad.unam.mx",
        "contrasena": "password123"
    }
    response = requests.post(f"{BASE_URL}/auth/register/unam", json=data)
    print("Registro UNAM:", response.json())

def test_register_externo():
    data = {
        "correo": "test@gmail.com",
        "contrasena": "password123"
    }
    response = requests.post(f"{BASE_URL}/auth/register/externo", json=data)
    print("Registro Externo:", response.json())

def test_login():
    data = {
        "correo": "test@comunidad.unam.mx",
        "contrasena": "password123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=data)
    print("Login:", response.json())

if __name__ == "__main__":
    print("Probando endpoints del MS-Ingreso...")
    print("Asegúrate de que el servidor esté ejecutándose en localhost:8000")
    print()
    
    try:
        test_register_unam()
        test_register_externo()
        test_login()
    except requests.exceptions.ConnectionError:
        print("Error: No se puede conectar al servidor. Asegúrate de que esté ejecutándose.")
    except Exception as e:
        print(f"Error: {e}")