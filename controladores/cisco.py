from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def getOfertasCisco(driver,indice,ofertas):
    #url="https://jobs.cisco.com/jobs/SearchJobs/internship?21178=%5B102674%5D&21178_format=6020&21179=%5B12229585%5D&21179_format=6021&listFilterMode=1"
    url="https://jobs.cisco.com/jobs/SearchJobs/internship?21178=%5B102674%5D&21178_format=6020&21179=%5B12229443%5D&21179_format=6021&listFilterMode=1"
    try:
        driver.get(url)
    except Exception as e:
        print(f"Error al abrir la página de Cisco")
        return indice, False
    # Espera a que cargue el contenedor con los listados de ofertas
    print("Esperando a que carguen las ofertas de Cisco...")
    ofertasTmp=[]
    try:
        wait = WebDriverWait(driver, 30)
        # Espera a que el contenedor esté presente en el DOM
        job_results_container = wait.until(EC.presence_of_element_located((By.ID, "content")))

        rows = job_results_container.find_elements(By.TAG_NAME, "tr")
        if rows[1].text=="No results":
            print(f"Se encontraron 0 ofertas de empleo en Cisco")
            return indice, True
    except Exception as e:
        print(f"Error al cargar los elementos de la página de Cisco")
        return indice, False
    # Iteramos sobre cada oferta y extraemos la información
    for index, row in enumerate(rows, start=1):
        if index==1:
            continue
        try:
            # Extraer el título del trabajo (por ejemplo, en un <h2> con clase 'job-title')
            columnas = row.find_elements(By.TAG_NAME, "td")
            
            job_title=columnas[0].text
            job_location=columnas[3].text
            if job_location !="Guadalajara, Mexico":
                continue
            job_link = columnas[0].find_element(By.TAG_NAME, "a").get_attribute("href")




            oferta="\nEmpresa: Cisco"+"\n"+"  Título: "+job_title+"\n"+"  Ubicación: "+job_location+"\n"+"  Link: "+job_link
            ofertasTmp.append(oferta)
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
    print(f"Se encontraron {len(ofertasTmp)} ofertas de empleo en Cisco")
    for i, oferta in enumerate(ofertasTmp):
        oferta="Oferta: "+str(i+indice+1)+oferta
        ofertas.append(oferta)   
    return indice+len(ofertasTmp), True


    

