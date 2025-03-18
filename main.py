from selenium import webdriver
from controladores.intel import getOfertasIntel
from controladores.oracle import getOfertasOracle
from controladores.hp import getOfertasHP
from controladores.ibm import getOfertasIBM
from controladores.cisco import getOfertasCisco
from controladores.c3 import getOfertasC3
from procesamiento import procesarOfertas

options = webdriver.ChromeOptions()
#options.add_argument("--start-maximized")
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

if __name__ == "__main__":
    index=int(0)
    ofertas=[]
    index = getOfertasCisco(driver, index, ofertas)
    index = getOfertasIntel(driver, index, ofertas)
    index = getOfertasHP(driver, index, ofertas)
    index = getOfertasOracle(driver, index, ofertas)
    index=getOfertasC3(driver, index, ofertas)
    index=getOfertasIBM(driver, index, ofertas)

    #JABIL
    #MICROSOFT
    #Bosch
    #CompuTrabajo
    print(f"Se encontraron {len(ofertas)} ofertas en total.")
    procesarOfertas(ofertas)
    """

    """
    driver.quit()