from selenium import webdriver
from controladores.intel import getOfertasIntel
from controladores.oracle import getOfertasOracle

options = webdriver.ChromeOptions()
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

if __name__ == "__main__":
    index=0
    ofertas = getOfertasOracle(driver,index)
    print("Ofertas Oracle:")
    for oferta in ofertas:
        print(oferta)
    ofertas = getOfertasIntel(driver,index)
    print("--------------------------------")
    print("Ofertas Intel:")
    for oferta in ofertas:
        print(oferta)
    print("Fin del programa")
    driver.quit()