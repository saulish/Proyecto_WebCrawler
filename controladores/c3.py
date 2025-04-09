from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def getOfertasC3(driver, indice,ofertas):
    url = "https://c3.ai/careers/"
    try:
        driver.get(url)
    except Exception as e:
        print(f"Error al cargar la página de C3.AI")
        return indice, False
    # Espera a que cargue el contenedor con los listados de ofertas
    print("Esperando a que carguen las ofertas de C3.AI...")
    try:      
        wait = WebDriverWait(driver, 30)
        # Paso 1: Ubicar el contenedor del selector de ubicación
        location_container = wait.until(
            EC.presence_of_element_located((By.ID, "opportunities"))
        )
        # Paso 2: Hacer click en el div que muestra "All locations"
        driver.execute_script("arguments[0].scrollIntoView(true);", location_container)
        select_selected = location_container.find_element(By.CSS_SELECTOR, "div.select-selected")
        select_selected.click()
        # Paso 3: Esperar a que el dropdown se expanda (se remueva la clase 'select-hide')
        wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.custom-select-div.location-select div.select-items:not(.select-hide)"))
        )

        # Paso 4: Buscar y hacer click en la opción "Guadalajara, Mexico"
        option_guadalajara = location_container.find_element(By.CSS_SELECTOR, "div.select-items div[data-id='4046390002']")
        option_guadalajara.click()

        # Paso 5: Esperar a que la selección se actualice (por ejemplo, que el texto del selector cambie a "Guadalajara, Mexico")
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, "div.custom-select-div.location-select div.select-selected"), "Guadalajara, Mexico")
        )
        # Paso 5.5 para mostrar todos los resultados
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='jobBtnHolder']//button")))
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        button.click()
        
        # Paso 6: Ubicar el contenedor de departamentos
        departments_container = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.departments_container.hide-for-small-only"))
        )

        try:
        # Paso 7: Dentro del contenedor, buscar y hacer click en el elemento de "Internships"
            internships_element = departments_container.find_element(By.CSS_SELECTOR, "h4.side_heading[data-id='4106281002']")
            driver.execute_script("arguments[0].scrollIntoView(true);", internships_element)
            internships_element.click()
        except Exception as e:
            print("En C3.AI no hay Internships disponibles o el elemento no se encontró.")
            return indice, True

    except Exception as e:
        print(f"Error al encontrar los elementos")
        return indice, False

    # Supongamos que los listados se encuentran en un contenedor con id 'job-results'
    # (ajusta el selector según el HTML real)
    try:

        job_results_container = wait.until(EC.presence_of_element_located((By.ID, "job_cards_container")))

        # Una vez cargado el contenedor, buscamos cada tarjeta de oferta
        # Por ejemplo, si cada oferta está en un <div> con la clase 'job-card'
        job_cards = job_results_container.find_elements(By.CSS_SELECTOR, "div.job_card")

        print(f"Se encontraron {len(job_cards)} ofertas de empleo en C3.AI")
    except Exception as e:
        print(f"Error al cargar las ofertas de C3.AI")
        return indice, False

    # Iteramos sobre cada oferta y extraemos la información
    for index, card in enumerate(job_cards, start=1):
        try:
            # Extraer el título del trabajo (por ejemplo, en un <h2> con clase 'job-title')
            job_title=card.find_element(By.CLASS_NAME, "title").text
            job_location=card.find_element(By.CLASS_NAME, "location").text
            
           
            # Extraer el enlace a la oferta (suponiendo que se encuentre en un <a>)
            job_link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
            oferta="Oferta: "+str(index+indice)+"\nEmpresa: C3.AI"+"\n"+"  Título: "+job_title+"\n"+"  Ubicación: "+job_location+"\n"+"  Link: "+job_link
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