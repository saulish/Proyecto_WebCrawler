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


def generar_msj(lista_empresas, json_path='ofertas.json'):
    """
    Lee el archivo JSON ubicado en 'json_path' y genera un informe en forma de string
    que contiene la información de las ofertas para cada empresa presente en 'lista_empresas'.
    
    El JSON se asume estructurado como:
    
    {
        "Empresa1": {
            "Título Oferta 1": {
                "Ubicacion": "...",
                "Link": "..."
            },
            "Título Oferta 2": {
                "Ubicacion": "...",
                "Link": "..."
            },
            ...
        },
        "Empresa2": {
            ...
        }
    }
    
    Para cada empresa en la lista se agrega al informe un encabezado y luego se listan las ofertas.
    
    Args:
        json_path (str): Ruta al archivo JSON con la información de ofertas.
        lista_empresas (list): Lista de nombres de empresas a incluir en el informe.
    
    Returns:
        str: Un string que contiene toda la información estructurada de las ofertas.
    """
    try:
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except Exception as e:
        return f"Error al cargar el archivo JSON: {e}"
    
    informe = ""
    for empresa in lista_empresas:
        informe += f"Empresa: {empresa}\n"
        # Verificar si la empresa existe en el JSON
        if empresa in data:
            ofertas = data[empresa]
            for titulo, detalles in ofertas.items():
                ubicacion = detalles.get("Ubicacion", "N/A")
                link = detalles.get("Link", "N/A")
                
                informe += f"  Título: {titulo}\n"
                informe += f"    Ubicación: {ubicacion}\n"
                informe += f"    Link: {link}\n"
            informe += "\n"  # Línea en blanco para separar empresas
        else:
            informe += "  No se encontraron ofertas para esta empresa.\n\n"
    
    return informe
