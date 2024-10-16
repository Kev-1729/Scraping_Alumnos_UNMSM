from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import csv

web_side = "http://websecgen.unmsm.edu.pe/carne/carne.aspx"
path = "C:\Program Files (x86)\chromedriver.exe"

driver = webdriver.Chrome(service=Service(path))
driver.get(web_side)

datos_totales = []
nombre_archivo = "FISI_prueba.csv"

for codigo in range(21200000,21200305):
    
    time.sleep(0.5)
    driver.execute_script(f"document.querySelector('#ctl00_ContentPlaceHolder1_txtUsuario').value = '{codigo}'")
    
    driver.execute_script("document.querySelector('#ctl00_ContentPlaceHolder1_cmdConsultar').click();")

    facultad = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_txtFacultad").get_attribute("value")

    time.sleep(0.5)
    if(facultad != ""):
        escuela = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_txtPrograma").get_attribute("value")
        nombre = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_txtAlumno").get_attribute("value")
        datos_totales.append([codigo, escuela, nombre])
    else:   
        continue

with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo_csv:
    escritor_csv = csv.writer(archivo_csv)
    
    for datos_iteracion in datos_totales:
        escritor_csv.writerow(datos_iteracion)