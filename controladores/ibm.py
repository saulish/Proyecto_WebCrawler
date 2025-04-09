from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def getOfertasIBM(driver,indice,ofertas):
    url="https://www.ibm.com/mx-es/careers/search?field_keyword_18[0]=Intern&field_keyword_18[1]=Internship&field_keyword_05[0]=Mexico"
    try:
        driver.get(url)
    except Exception as e:
        print(f"Error al abrir la página de IBM")
        return indice, False
    # Espera a que cargue el contenedor con los listados de ofertas
    print("Esperando a que carguen las ofertas de IBM...")
    ofertasTemp=[] #Lista temporal para almacenar las ofertas de mx en general
    wait = WebDriverWait(driver, 30)
    try:
        job_results_container = wait.until(EC.presence_of_element_located((By.ID, "ibm-hits-wrapper")))
        job_cards = job_results_container.find_elements(By.CLASS_NAME, "bx--card-group__cards__col")
    except Exception as e:
        print(f"Error al obtener los elementos de IBM")
        return indice, False

    # Iteramos sobre cada oferta y extraemos la información
    for index, card in enumerate(job_cards, start=1):
        try:
            # Extraer el título del trabajo (por ejemplo, en un <h2> con clase 'job-title')
            job_title = card.find_element(By.CLASS_NAME, "bx--card__heading").text
            
            # Extraer la dirección o ubicación (por ejemplo, en un <span> con clase 'job-location')
            job_location = card.find_element(By.CLASS_NAME, "ibm--card__copy__inner").text.split("\n")[1]
            if job_location!="GUADALAJARA, MX" and job_location!="El Salto, MX":
                continue
            #
            # Extraer el enlace a la oferta (suponiendo que se encuentre en un <a>)
            job_link = card.find_element(By.CLASS_NAME, "bx--card-group__card").get_attribute("href")

            oferta="\nEmpresa: IBM"+"\n"+"  Título: "+job_title+"\n"+"  Ubicación: "+job_location+"\n"+"  Link: "+job_link
            ofertasTemp.append(oferta)
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
    print(f"Se encontraron {len(ofertasTemp)} ofertas de empleo en IBM")
    for i,card in enumerate(ofertasTemp):
        card="Oferta: "+str(i+indice+1)+card
        ofertas.append(card)
    
    return indice+len(ofertasTemp), True


    

