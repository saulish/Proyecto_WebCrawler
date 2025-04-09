import json

def procesarOfertas(ofertas):
    """
    Procesa una lista de strings donde cada string representa una oferta con el formato:
    
        Oferta 8:
        Empresa: Oracle
          Título: ...
          Ubicación: ...
          Link: ...
    
    Genera un archivo JSON ('ofertas.json') estructurado como:
    
    {
        "Oracle": {
            "Fresh Graduated - Python Developer for AI Technologies": {
                "Ubicacion": "...",
                "Link": "..."
            }
        },
        ...
    }
    """
    structured_offers = {}

    for oferta in ofertas:
        lines = [line.strip() for line in oferta.splitlines() if line.strip()]

        if len(lines) < 5:
            print("Advertencia: La oferta no tiene suficientes líneas para procesarse:")
            print(oferta)
            continue

        try:
            empresa = lines[1].split(":", 1)[1].strip() if ":" in lines[1] else ""
            titulo = lines[2].split(":", 1)[1].strip() if ":" in lines[2] else ""
            ubicacion = lines[3].split(":", 1)[1].strip() if ":" in lines[3] else ""
            link = lines[4].split(":", 1)[1].strip() if ":" in lines[4] else ""

            if empresa not in structured_offers:
                structured_offers[empresa] = {}
            
            structured_offers[empresa][titulo] = {
                "Ubicacion": ubicacion,
                "Link": link
            }
        except Exception as e:
            print("Error procesando la oferta:")
            print(oferta)
            print(e)

    with open("ofertas.json", "w", encoding="utf-8") as file:
        json.dump(structured_offers, file, indent=4, ensure_ascii=False)

    print("¡Archivo JSON generado correctamente con estructura [empresa][titulo]!")
