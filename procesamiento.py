import json

def procesarOfertas(ofertas):
    """
    Procesa una lista de strings donde cada string representa una oferta con el siguiente formato:
    
        Oferta 8:
        Empresa: Oracle
          Título: Fresh Graduated - Python Developer for AI Technologies
          Ubicación: ZAPOPAN, JALISCO, Mexico and 1 more
          Link: https://careers.oracle.com/jobs/...
    
    Genera un archivo JSON ('ofertas.json') con cada oferta convertida a un diccionario.
    """
    processed_offers = []
    
    for oferta in ofertas:
        # Dividir la oferta en líneas y eliminar espacios en blanco
        lines = [line.strip() for line in oferta.splitlines() if line.strip()]
        
        # Se espera que haya al menos 5 líneas: Oferta, Empresa, Título, Ubicación y Link
        if len(lines) < 5:
            print("Advertencia: La oferta no tiene suficientes líneas para procesarse:")
            print(oferta)
            continue
        
        try:
            # Extraer los datos de la oferta
            numero = lines[0].split(":", 1)[1].strip() if ":" in lines[0] else ""
            empresa = lines[1].split(":", 1)[1].strip() if ":" in lines[1] else ""
            titulo = lines[2].split(":", 1)[1].strip() if ":" in lines[2] else ""
            ubicacion = lines[3].split(":", 1)[1].strip() if ":" in lines[3] else ""
            link = lines[4].split(":", 1)[1].strip() if ":" in lines[4] else ""
            
            processed_offers.append({
                "Número": numero,
                "Empresa": empresa,
                "Título": titulo,
                "Ubicación": ubicacion,
                "Link": link
            })
        except Exception as e:
            print("Error procesando la oferta:")
            print(oferta)
            print(e)
    
    # Guardar la lista de ofertas procesadas en un archivo JSON
    with open("ofertas.json", "w", encoding="utf-8") as file:
        json.dump(processed_offers, file, indent=4, ensure_ascii=False)
    
    print("¡Archivo JSON generado correctamente en 'ofertas.json'!")