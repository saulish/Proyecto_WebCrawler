from selenium import webdriver
from controladores.intel import getOfertasIntel
from controladores.oracle import getOfertasOracle
from controladores.hp import getOfertasHP
from controladores.ibm import getOfertasIBM
from controladores.cisco import getOfertasCisco
from procesamiento import procesarOfertas

options = webdriver.ChromeOptions()
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

if __name__ == "__main__":
    index=int(0)
    ofertas=[]
    index = getOfertasCisco(driver, index, ofertas)
    index=getOfertasIBM(driver, index, ofertas)
    index = getOfertasIntel(driver, index, ofertas)
    index = getOfertasHP(driver, index, ofertas)
    index = getOfertasOracle(driver, index, ofertas)
    #C3
    #JABIL
    #MICROSOFT
    #Bosch
    #CompuTrabajo
    print(f"Se encontraron {len(ofertas)} ofertas en total.")
    procesarOfertas(ofertas)
    """

    """
    driver.quit()