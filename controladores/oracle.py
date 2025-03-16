from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def getOfertasOracle(driver,indice):
    url="https://careers.oracle.com/jobs/#en/sites/jobsearch/requisitions?keyword=Internship&location=ZAPOPAN%2C+JALISCO%2C+Mexico&locationId=300000313566531&locationLevel=city&mode=location&radius=25&radiusUnit=KM"
    driver.get(url)
    ofertas=[]
    # Espera a que cargue el contenedor con los listados de ofertas
    print("Esperando a que carguen las ofertas...")
    wait = WebDriverWait(driver, 15)

    
    job_results_container = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "jobs-grid__list")))
    jobs_links = job_results_container.find_elements(By.TAG_NAME, "a")

    job_cards = job_results_container.find_elements(By.CLASS_NAME, "job-grid-item__content")

    print(f"Se encontraron {len(job_cards)} ofertas de empleo:")

    # Iteramos sobre cada oferta y extraemos la información
    for index, card in enumerate(job_cards, start=1):
        try:
            # Extraer el título del trabajo (por ejemplo, en un <h2> con clase 'job-title')
            job_title = card.find_element(By.CLASS_NAME, "job-tile__header-container").text
            
            # Extraer la dirección o ubicación (por ejemplo, en un <span> con clase 'job-location')
            job_location = card.find_element(By.CLASS_NAME, "job-list-item__job-info-value").text
            #
            # Extraer el enlace a la oferta (suponiendo que se encuentre en un <a>)
            job_link = jobs_links[index].get_attribute("href")

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
