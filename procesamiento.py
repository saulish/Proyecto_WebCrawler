import json
import os
def procesarOfertas(ofertas):
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

    

    print("¡Mensaje estructurado a la perfeccion!")
    return structured_offers

def crearJson(ofertas, json_path='ofertas.json'):
    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(ofertas, file, indent=4, ensure_ascii=False)


def generar_msj(lista_empresas, json_path='ofertas.json'):
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


def verificarJson(name="ofertas.json"):
    return os.path.exists(name)


def jsonToString(data: dict) -> str:

    return json.dumps(data, indent=4, ensure_ascii=False)


def formatearSeccion(heading: str, ofertas: dict) -> str:
    """Recorre el diccionario de ofertas y retorna un string formateado con un encabezado."""
    mensaje_list = [f"{heading}\n" + "-" * len(heading)]
    for empresa, lista in ofertas.items():
        mensaje_list.append(f"Empresa: {empresa}")
        for titulo, detalles in lista.items():
            oferta_str = (
                f"  Título: {titulo}\n"
                f"  Ubicación: {detalles.get('Ubicacion', 'N/A')}\n"
                f"  Link: {detalles.get('Link', 'N/A')}\n"
            )
            mensaje_list.append(oferta_str)
        mensaje_list.append("")  # Línea en blanco para separar empresas
    return "\n".join(mensaje_list)


def updateJson(ofertasProcesadas: dict, empresaError: list, archivo="ofertas.json") -> str:
    # Convertir el diccionario a string JSON usando jsonToString
    ofertasProcesadas_str = jsonToString(ofertasProcesadas)
    
    # Intentar leer el archivo JSON existente
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            json_antiguo_str = f.read().strip()
    except Exception as e:
        print("Error al leer el archivo JSON existente:", e)
        json_antiguo_str = ""
    
    # Comparar si el contenido es idéntico
    if json_antiguo_str == ofertasProcesadas_str:
        print("No hay nuevas ofertas. El JSON no ha cambiado.")
        return ""
    
    # Parsear a diccionario para comparación estructural
    try:
        data_nueva = ofertasProcesadas  # ya es dict
        data_antigua = json.loads(json_antiguo_str) if json_antiguo_str else {}
    except Exception as e:
        print("Error al parsear los datos JSON:", e)
        return ""
    
    # Incorporar al nuevo JSON las empresas que fallaron (tomándolas del JSON antiguo)
    for empresa in empresaError:
        if empresa in data_antigua:
            data_nueva[empresa] = data_antigua[empresa]
    
    # Detectar las nuevas ofertas (aquellas que están en data_nueva pero no en data_antigua)
    nuevas_ofertas = {}
    for empresa, ofertas in data_nueva.items():
        if empresa not in data_antigua:
            nuevas_ofertas[empresa] = ofertas
        else:
            for titulo, detalles in ofertas.items():
                if titulo not in data_antigua[empresa]:
                    if empresa not in nuevas_ofertas:
                        nuevas_ofertas[empresa] = {}
                    nuevas_ofertas[empresa][titulo] = detalles
                    
    # Si no se encontraron nuevas ofertas
    if nuevas_ofertas == {}:
        print("No se encontraron nuevas ofertas.")
        try:                                                #ACTUALIZAMOS EL JSON DE IGUAL FORMA POR SI SE ELIMINO ALGUNA VACANTE
            with open(archivo, "w", encoding="utf-8") as f:
                f.write(jsonToString(data_nueva))
        except Exception as e:
            print("Error al actualizar el archivo JSON:")
        return ""
    
    # Determinar las ofertas que ya existían (vacantes pasadas disponibles)
    ofertas_pasadas = {}
    for empresa, ofertas in data_nueva.items():
        for titulo, detalles in ofertas.items():
            if empresa in nuevas_ofertas and titulo in nuevas_ofertas.get(empresa, {}):
                # Oferta nueva; se omite aquí.
                continue
            else:
                if empresa not in ofertas_pasadas:
                    ofertas_pasadas[empresa] = {}
                ofertas_pasadas[empresa][titulo] = detalles
    
    # Actualizar el archivo JSON con el nuevo contenido
    try:
        with open(archivo, "w", encoding="utf-8") as f:
            f.write(jsonToString(data_nueva))
        print("Archivo JSON actualizado con las nuevas ofertas.")
    except Exception as e:
        print("Error al actualizar el archivo JSON:")
    
    # Generar las dos secciones en HTML
    seccion_nuevas = formatearOfertas("Nuevas vacantes", nuevas_ofertas)
    seccion_pasadas = formatearOfertas("Vacantes pasadas disponibles aún", ofertas_pasadas)
    
    # Armar el mensaje final en HTML
    mensaje_html = (
        "<html><body style='font-family: Arial, sans-serif;'>\n" +
        seccion_nuevas +
        "\n<br><br>\n" +
        seccion_pasadas +
        "\n</body></html>"
    )
    
    return mensaje_html


def formatearOfertas(heading: str, ofertas: dict) -> str:
    mensaje_list = []
    # Agregar el heading de la sección
    mensaje_list.append(f"<h3 style='color: #2c3e50;'>{heading}</h3>")
    
    # Recorrer cada empresa y sus ofertas
    for empresa, ofertas_empresa in ofertas.items():
        # Nombre de la empresa en un encabezado grande
        mensaje_list.append(f"<h2 style='color: #2c3e50;'>{empresa}</h2>")
        for titulo, detalles in ofertas_empresa.items():
            # El título en negrita
            mensaje_list.append(f"<p><strong>{titulo}</strong></p>")
            # Ubicación
            mensaje_list.append(f"<p>Ubicación: {detalles.get('Ubicacion', 'N/A')}</p>")
            # Enlace formateado como botón "Aplica aquí"
            link = detalles.get('Link', '#')
            mensaje_list.append(
                f"<p><a href='{link}' style='background-color: #3498db; color: #fff; padding: 8px 12px; "
                f"text-decoration: none; border-radius: 4px;' target='_blank'>Aplica aquí</a></p>"
            )
            # Separador horizontal para mayor legibilidad
            mensaje_list.append("<hr style='border: 0; border-top: 1px solid #eee;'>")
    
    return "\n".join(mensaje_list)

