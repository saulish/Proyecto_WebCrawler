from selenium import webdriver
from controladores.intel import getOfertasIntel
from controladores.oracle import getOfertasOracle
from controladores.hp import getOfertasHP
from controladores.ibm import getOfertasIBM
from controladores.cisco import getOfertasCisco
from controladores.c3 import getOfertasC3
from procesamiento import procesarOfertas, generar_msj, verificarJson, crearJson,updateJson, jsonToString, formatearOfertas
from mail import sendMail, usuarios
import time

empresas=['HP', 'C3', 'Intel', 'IBM', 'Cisco','Oracle']
intentos = {empresa: 0 for empresa in empresas}
options = webdriver.ChromeOptions()
#options.add_argument("--start-maximized")
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

def enviarOfertas(mail):
    for nuevos in usuarios['new']:
        print(f"Enviando correo a {nuevos}")
        sendMail(mail,nuevos)
    for olds in usuarios['old']:
        sendMail(mail,olds)
    print("Se han enviado las ofertas por correo electrónico.")

def getofertas(empresa, index, ofertas, tmpEmpresas):
    match empresa:
        case 'HP':
            index, estado = getOfertasHP(driver, index, ofertas)
            if estado == True:
                print("Ofertas de HP procesadas")
                tmpEmpresas.remove(empresa)
            else:
                tmpEmpresas.remove(empresa)
                tmpEmpresas.append(empresa)     # MANDAMOS A LA EMPRESA HASTA EL FINAL
                intentos[empresa] += 1
                print(f"Error al procesar ofertas de HP, intento {intentos[empresa]}")

        case 'C3':  
            index, estado = getOfertasC3(driver, index, ofertas)
            if estado == True:
                print("Ofertas de C3 procesadas")
                tmpEmpresas.remove(empresa)
            else:
                print("Error al procesar ofertas de C3")
                tmpEmpresas.remove(empresa)
                tmpEmpresas.append(empresa)     # MANDAMOS A LA EMPRESA HASTA EL FINAL
                intentos[empresa] += 1
                print(f"Error al procesar ofertas de C3, intento {intentos[empresa]}")
        case 'Intel':
            index, estado= getOfertasIntel(driver, index, ofertas)
            if estado == True:
                print("Ofertas de Intel procesadas")
                tmpEmpresas.remove(empresa)
            else:
                tmpEmpresas.remove(empresa)
                tmpEmpresas.append(empresa)     # MANDAMOS A LA EMPRESA HASTA EL FINAL
                intentos[empresa] += 1
                print(f"Error al procesar ofertas de Intel, intento {intentos[empresa]}")
        case 'IBM':
            index, estado = getOfertasIBM(driver, index, ofertas)
            if estado == True:
                print("Ofertas de IBM procesadas")
                tmpEmpresas.remove(empresa)
            else:
                tmpEmpresas.remove(empresa)
                tmpEmpresas.append(empresa)     # MANDAMOS A LA EMPRESA HASTA EL FINAL
                intentos[empresa] += 1
                print(f"Error al procesar ofertas de IBM, intento {intentos[empresa]}")

        case 'Cisco':
            index, estado = getOfertasCisco(driver, index, ofertas)
            if estado == True:
                print("Ofertas de Cisco procesadas")
                tmpEmpresas.remove(empresa)
            else:
                tmpEmpresas.remove(empresa)
                tmpEmpresas.append(empresa)     # MANDAMOS A LA EMPRESA HASTA EL FINAL
                intentos[empresa] += 1
                print(f"Error al procesar ofertas de Cisco, intento {intentos[empresa]}")
        case 'Oracle':
            index, estado = getOfertasOracle(driver, index, ofertas)
            if estado == True:
                print("Ofertas de Oracle procesadas")
                tmpEmpresas.remove(empresa)
            else:
                tmpEmpresas.remove(empresa)
                tmpEmpresas.append(empresa)     # MANDAMOS A LA EMPRESA HASTA EL FINAL
                intentos[empresa] += 1
                print(f"Error al procesar ofertas de Oracle, intento {intentos[empresa]}")
        case _: 
            print(f"Empresa {empresa} no reconocida")
            #intentos[empresa] += 1

def mainOfertas(empresasError):
    index=int(0)
    _=0
    ofertas=[]
    maxIntentos=3
    tmpEmpresas = empresas.copy()
    #"""  
    
    while len(tmpEmpresas) > 0:
        if _%3==0 and _!=0:
            print("Esperando 5 segundos para evitar bloqueos...")
            time.sleep(5)
        empresa = tmpEmpresas[0]
        getofertas(empresa, index, ofertas, tmpEmpresas)
        if intentos[empresa] >= maxIntentos:
            tmpEmpresas.remove(empresa)
            print(f"Se han hecho 3 intentos fallidos para {empresa}. Se eliminará de la lista.")
            empresasError.append(empresa)           #AÑADIMOS LA EMPRESA A UNA LISTA PARA EVITAR QUE SE PROCESEN LUEGO COMO NUEVAS
        _+=1
    return ofertas


if __name__ == "__main__":
    intervalo=3600        #DEFINIMOS UN INTERVALO DE TIEMPO PARA EL ENVIO DE LOS CORREOS
    while True:
        empresasError=[]    #ALMACENAREMOS AQUELLAS EMPRESAS QUE NO SE PUEDAN PROCESAR
        intentos = {empresa: 0 for empresa in empresas}
        ofertas=mainOfertas(empresasError)
        print(f"Se han encontrado {len(ofertas)} ofertas de trabajo.")
        mensaje=""
        ofertasProcesadas=procesarOfertas(ofertas)        #RETORNA EL JSON COMO UN DICT
        if verificarJson():                             #SI EXISTE EL JSON
            mensaje=updateJson(ofertasProcesadas, empresasError)        #ACTUALIZA EL JSON CON LAS NUEVAS OFERTAS
            if mensaje=="":
                print("No se han encontrado nuevas ofertas.")
                print(f"Esperando {intervalo} segundos para la siguiente verificación...")
                time.sleep(intervalo) 
                continue
        else:
            crearJson(ofertasProcesadas)                #TOMA LAS OFERTAS Y CREA EL JSON
            seccion=formatearOfertas("Ofertas encontradas",ofertasProcesadas)    #TOMA EL DICT Y LO CONVIERTE EN UN STRING FORMATEADO
            mensaje= (
                "<html><body style='font-family: Arial, sans-serif;'>\n" +
                seccion +
                "\n<br><br>\n" +
                "\n</body></html>"
            )                                           #AÑADE LOS HEADERS Y BODY DEL HTML
        enviarOfertas(mensaje)          #ENVIA EL CORREO


        print(f"Esperando {intervalo} segundos para la siguiente verificación...")
        time.sleep(intervalo)       #CADA INTERVALO VECES VAMOS A REALIZAR LA PETICION DE LOS OFERTAS Y ENVIAR LOS CORREOS
    #"""
    #JABIL
    #MICROSOFT
    #Bosch
    #CompuTrabajo
    driver.quit()