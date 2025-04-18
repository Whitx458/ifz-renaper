from flask import Flask, jsonify
import requests
import logging

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/api/ricardo/<dni>', methods=['GET'])
def consulta_dni(dni):
    login_url = "https://informescea.com.ar/login.php"
    consulta_url = "https://informescea.com.ar/api.php?method=getPerson"
    
    payload_login = {
        "username": "AGILCRED SA.",
        "password": "GERENCIA"
    }

    session = requests.Session()
    response_login = session.post(login_url, data=payload_login)

    if response_login.status_code == 200:
        print("Inicio de sesión exitoso")

        payload_consulta = {
            "id": "39414730",
            "dni": dni,
            "cuit": None,
            "sexo": None
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Accept": "application/json, text/javascript, /; q=0.01",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://informescea.com.ar/",
            "Referer": "https://informescea.com.ar/index.php",
            "X-Requested-With": "XMLHttpRequest"
        }

        response_consulta = session.post(consulta_url, data=payload_consulta, headers=headers)

        if response_consulta.status_code == 200:
            print("Consulta exitosa!")
            json_response = response_consulta.json()
            return jsonify(json_response), 200
        else:
            print(f"Error en la consulta: {response_consulta.status_code}")
            return jsonify({"error": "Error en la consulta"}), response_consulta.status_code

    else:
        print(f"Error en el inicio de sesión: {response_login.status_code}")
        return jsonify({"error": "Error en el inicio de sesión"}), response_login.status_code

if __name__ == '__main__':
    print("Iniciando la aplicación Flask...")
    app.run(debug=False) 
