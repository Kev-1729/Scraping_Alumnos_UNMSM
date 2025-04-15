from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

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
    
    for codigo in range(rango_inicial, rango_final+1):
        time.sleep(0.5)
        datos_codigo = obtener_datos_por_codigo(codigo, driver)
        
        if datos_codigo:
            datos.append(datos_codigo)
    
    return datos

def main():
    inicio = int(input("Desde: "))
    final = int(input("Hasta: "))
    # inicio tiene que ser menor que final
    driver = init_driver()
    web_site = "http://websecgen.unmsm.edu.pe/carne/carne.aspx"
    driver.get(web_site)
    datos = obtener_datos(driver, inicio, final)
    driver.quit()
    
    # Guardar en un archivo JSON
    with open("datos.json", "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()
