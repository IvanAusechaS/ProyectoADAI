from estrategia1 import Encuesta, Tema, Pregunta, Encuestado

def leer_archivo_txt(ruta):
    with open(ruta, 'r', encoding='utf-8') as f:
        lineas = [line.rstrip("\n") for line in f]

    encuesta = Encuesta()
    idx = 0
    id_auto = 1

    # Leer encuestados hasta la primera línea que empieza con "{"
    while idx < len(lineas) and not lineas[idx].strip().startswith("{"):
        linea = lineas[idx].strip()
        if "," in linea and "Experticia:" in linea and "Opinión:" in linea:
            nombre = linea.split(",")[0].strip()
            partes = linea.split(",")
            exp = int(partes[1].split(":")[1].strip())
            op = int(partes[2].split(":")[1].strip())
            encuesta.registrar_encuestado(Encuestado(id_auto, nombre, exp, op))
            id_auto += 1
        idx += 1

    # Leer bloques { } por temas, separados por líneas en blanco
    tema_num = 1
    while idx < len(lineas):
        # saltar líneas en blanco iniciales
        while idx < len(lineas) and not lineas[idx].strip():
            idx += 1
        if idx >= len(lineas):
            break

        tema = Tema(f"Tema {tema_num}")
        pregunta_num = 1

        while idx < len(lineas) and lineas[idx].strip():
            bloque = lineas[idx].strip()
            if bloque.startswith("{"):
                ids_str = bloque.strip("{} ")
                ids = [int(x.strip()) for x in ids_str.split(",")] if ids_str else []
                pregunta = Pregunta(f"{tema_num}.{pregunta_num}")
                for eid in ids:
                    if eid in encuesta.encuestados_dict:
                        pregunta.agregar_encuestado(encuesta.encuestados_dict[eid])
                pregunta.ordenar_encuestados()
                tema.agregar_pregunta(pregunta)
                pregunta_num += 1
            idx += 1

        tema.ordenar_preguntas()
        encuesta.agregar_tema(tema)
        tema_num += 1

    encuesta.ordenar_temas()
    return encuesta
