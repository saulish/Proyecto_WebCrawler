from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def getOfertasIntel(driver, indice,ofertas):
    url = "https://jobs.intel.com/en/search-jobs/internship/Guadalajara%2C%20Jalisco/599/1/4/3996063-4004156-8582140-4005539/20x66682/-103x39182/50/2"
    driver.get(url)
    # Espera a que cargue el contenedor con los listados de ofertas
    print("Esperando a que carguen las ofertas...")
    try:
        wait = WebDriverWait(driver, 15)
    except Exception as e:
        print(f"Error al esperar por la página: {e}")

    # Supongamos que los listados se encuentran en un contenedor con id 'job-results'
    # (ajusta el selector según el HTML real)
    job_results_container = wait.until(EC.presence_of_element_located((By.ID, "search-results-list")))

    # Una vez cargado el contenedor, buscamos cada tarjeta de oferta
    # Por ejemplo, si cada oferta está en un <div> con la clase 'job-card'
    job_cards = job_results_container.find_elements(By.CLASS_NAME, "search-results-list-wrapper")

    print(f"Se encontraron {len(job_cards)} ofertas de empleo en Intel")

    # Iteramos sobre cada oferta y extraemos la información
    for index, card in enumerate(job_cards, start=1):
        try:
            # Extraer el título del trabajo (por ejemplo, en un <h2> con clase 'job-title')
            jobData = card.find_element(By.CLASS_NAME, "search-title-location").text.split("\n")
            job_title=jobData[0]
            job_location=jobData[1]
            
           
            # Extraer el enlace a la oferta (suponiendo que se encuentre en un <a>)
            job_link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
            oferta="Oferta: "+str(index+indice)+"\nEmpresa: Intel"+"\n"+"  Título: "+job_title+"\n"+"  Ubicación: "+job_location+"\n"+"  Link: "+job_link
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
    
    return indice+len(job_cards)
