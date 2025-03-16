from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def getOfertasIntel(driver, indice):
    url = "https://jobs.intel.com/en/search-jobs/internship/Guadalajara%2C%20Jalisco/599/1/4/3996063-4004156-8582140-4005539/20x66682/-103x39182/50/2"
    driver.get(url)
    ofertas=[]
    # Espera a que cargue el contenedor con los listados de ofertas
    print("Esperando a que carguen las ofertas...")
    wait = WebDriverWait(driver, 15)

    # Supongamos que los listados se encuentran en un contenedor con id 'job-results'
    # (ajusta el selector según el HTML real)
    job_results_container = wait.until(EC.presence_of_element_located((By.ID, "search-results-list")))

    # Una vez cargado el contenedor, buscamos cada tarjeta de oferta
    # Por ejemplo, si cada oferta está en un <div> con la clase 'job-card'
    job_cards = job_results_container.find_elements(By.CLASS_NAME, "search-results-list-wrapper")

    print(f"Se encontraron {len(job_cards)} ofertas de empleo:")

    # Iteramos sobre cada oferta y extraemos la información
    for index, card in enumerate(job_cards, start=1):
        try:
            # Extraer el título del trabajo (por ejemplo, en un <h2> con clase 'job-title')
            job_title = card.find_element(By.CLASS_NAME, "search-title-location").text
            
            # Extraer la dirección o ubicación (por ejemplo, en un <span> con clase 'job-location')
            job_location = card.find_element(By.CSS_SELECTOR, "span.job-location").text
            
            # Extraer el enlace a la oferta (suponiendo que se encuentre en un <a>)
            job_link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
            oferta="Oferta "+str(index+indice)+":\n"+"  Título: "+job_title+"\n"+"  Ubicación: "+job_location+"\n"+"  Link: "+job_link
            ofertas.append(oferta)
            """
            
            print(f"Oferta {index}:")
            print(f"  Título: {job_title}")
            print(f"  Ubicación: {job_location}")
            print(f"  Link: {job_link}")
            print("-" * 50)
            """
        except Exception as e:
            print(f"Error extrayendo datos de la oferta {index}: {e}")

    # Espera un poco antes de cerrar para observar resultados (opcional)
    time.sleep(5)
    
    return ofertas
