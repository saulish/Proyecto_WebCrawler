from selenium import webdriver
from controladorIntel import getOfertasIntel

options = webdriver.ChromeOptions()
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

if __name__ == "__main__":
    ofertas = getOfertasIntel(driver)
    for oferta in ofertas:
        print(oferta)
    print("Fin del programa")