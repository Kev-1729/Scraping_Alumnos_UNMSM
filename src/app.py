from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

app = Flask(__name__)

def init_driver():
    driver = webdriver.Edge()
    return driver

def obtener_datos_por_codigo(codigo, driver):
    driver.execute_script(f"document.querySelector('#ctl00_ContentPlaceHolder1_txtUsuario').value = '{codigo}'")
    driver.execute_script("document.querySelector('#ctl00_ContentPlaceHolder1_cmdConsultar').click();")
    
    time.sleep(0.5)

    facultad = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_txtFacultad").get_attribute("value")
    
    if facultad:
        escuela = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_txtPrograma").get_attribute("value")
        nombre = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_txtAlumno").get_attribute("value")
        return {
            "codigo": codigo,
            "escuela": escuela,
            "nombre": nombre
        }
    
    return None

def obtener_datos(driver, rango_inicial, rango_final):
    datos = []
    
    for codigo in range(rango_inicial, rango_final):
        time.sleep(0.5)
        datos_codigo = obtener_datos_por_codigo(codigo, driver)
        
        if datos_codigo:
            datos.append(datos_codigo)
    
    return datos

@app.route('/api/datos', methods=['GET'])
def api_datos():
    driver = init_driver()
    web_site = "http://websecgen.unmsm.edu.pe/carne/carne.aspx"
    driver.get(web_site)

    datos = obtener_datos(driver, 21200000, 21200015)
    
    driver.quit()
    return jsonify(datos)

if __name__ == '__main__':
    app.run(debug=True)
