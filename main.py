from selenium import webdriver
from controladores.intel import getOfertasIntel
from controladores.oracle import getOfertasOracle
from controladores.hp import getOfertasHP
from controladores.ibm import getOfertasIBM
from controladores.cisco import getOfertasCisco
from controladores.c3 import getOfertasC3
from procesamiento import procesarOfertas
import time

empresas=['HP', 'C3', 'Intel', 'IBM', 'Cisco','Oracle']
intentos = {empresa: 0 for empresa in empresas}
options = webdriver.ChromeOptions()
#options.add_argument("--start-maximized")
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
def getofertas(empresa, index, ofertas):
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


if __name__ == "__main__":
    index=int(0)
    _=0
    ofertas=[]
    maxIntentos=3
    tmpEmpresas = empresas.copy()
    while len(tmpEmpresas) > 0:
        if _%3==0 and _!=0:
            print("Esperando 5 segundos para evitar bloqueos...")
            time.sleep(5)
        empresa = tmpEmpresas[0]
        getofertas(empresa, index, ofertas)
        if intentos[empresa] >= maxIntentos:
            tmpEmpresas.remove(empresa)
            print(f"Se han hecho 3 intentos fallidos para {empresa}. Se eliminará de la lista.")
        _+=1
    print(f"Se han encontrado {len(ofertas)} ofertas de trabajo.")
    procesarOfertas(ofertas)
    #JABIL
    #MICROSOFT
    #Bosch
    #CompuTrabajo
    """
    index,_ = getOfertasOracle(driver, index, ofertas)
    index,_ = getOfertasHP(driver, index, ofertas)
    time.sleep(7)
    index,_ = getOfertasC3(driver, index, ofertas)
    index,_ = getOfertasIntel(driver, index, ofertas)
    time.sleep(7)
    index,_ = getOfertasIBM(driver, index, ofertas)
    index,_ = getOfertasCisco(driver, index, ofertas)
    procesarOfertas(ofertas)
    """
    driver.quit()