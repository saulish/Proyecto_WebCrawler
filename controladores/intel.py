from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def getOfertasIntel(driver, indice,ofertas):
    url = "https://intel.wd1.myworkdayjobs.com/en-US/External?q=internship&locations=1e4a4eb3adf101717b7c0175bf81decd"

    try:
        driver.get(url)
    except Exception as e:
        print(f"Error al cargar la página de Intel")
        return indice, False
    # Espera a que cargue el contenedor con los listados de ofertas
    print("Esperando a que carguen las ofertas de Intel...")
    try:
        wait = WebDriverWait(driver, 30)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "css-1q2dra3")))

        job_results_container = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "css-27w6p6")))  
        job_cards = job_results_container.find_elements(By.CLASS_NAME, "css-1q2dra3")
        print(f"Se encontraron {len(job_cards)} ofertas de empleo en Intel")

    except Exception as e:
        print(f"Error al encontrar los elementos de la pagina de Intel")  
        return indice, False

    # Iteramos sobre cada oferta y extraemos la información
    for index, card in enumerate(job_cards, start=1):
        try:
            # Extraer el título del trabajo (por ejemplo, en un <h2> con clase 'job-title')
            job_title=card.find_element(By.CLASS_NAME, "css-b3pn3b").text
            job_location=card.find_element(By.CLASS_NAME, "css-129m7dg").text       
            # Extraer el enlace a la oferta (suponiendo que se encuentre en un <a>)
            job_link = card.find_element(By.CLASS_NAME, "css-19uc56f").get_attribute("href")
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
    
    return indice+len(job_cards), True
