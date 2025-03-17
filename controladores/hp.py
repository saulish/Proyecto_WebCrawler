from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def getOfertasHP(driver,indice,ofertas):
    url="https://hp.wd5.myworkdayjobs.com/es/ExternalCareerSite?q=internship&primaryLocation=336ea9b27e9910b218d5896bc8f0e9c6"
    driver.get(url)
    # Espera a que cargue el contenedor con los listados de ofertas
    print("Esperando a que carguen las ofertas...")

    wait = WebDriverWait(driver, 30)
    # Espera a que el contenedor esté presente en el DOM
    job_results_container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".css-27w6p6")))
    
    # Espera hasta que el texto del contenedor ya no contenga "Loading"
    wait.until(lambda d: "Loading" not in d.find_element(By.CSS_SELECTOR, ".css-27w6p6").text)


    job_cards = job_results_container.find_elements(By.CSS_SELECTOR, "li.css-1q2dra3")
    

    jobs_links = job_results_container.find_elements(By.TAG_NAME, "a")

    print(f"Se encontraron {len(job_cards)} ofertas de empleo en HP")

    # Iteramos sobre cada oferta y extraemos la información
    for index, card in enumerate(job_cards, start=1):
        try:
            # Extraer el título del trabajo (por ejemplo, en un <h2> con clase 'job-title')
            job_title = card.find_element(By.CSS_SELECTOR, "a.css-19uc56f").text
            
            # Extraer la dirección o ubicación (por ejemplo, en un <span> con clase 'job-location')
            job_location = card.find_element(By.CSS_SELECTOR, "dd.css-129m7dg").text
            #
            # Extraer el enlace a la oferta (suponiendo que se encuentre en un <a>)
            job_link = card.find_element(By.CSS_SELECTOR, "a.css-19uc56f").get_attribute("href")

            oferta="Oferta: "+str(index+indice)+"\nEmpresa: HP"+"\n"+"  Título: "+job_title+"\n"+"  Ubicación: "+job_location+"\n"+"  Link: "+job_link
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


    

