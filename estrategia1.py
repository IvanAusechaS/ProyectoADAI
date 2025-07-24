# =========================
# ALGORITMO MERGE SORT CLÁSICO
# =========================

def merge_sort(lista):
    if len(lista) <= 1:
        return lista

    medio = len(lista) // 2
    izquierda = merge_sort(lista[:medio])
    derecha = merge_sort(lista[medio:])
    return merge(izquierda, derecha)

def merge(izq, der):
    resultado = []
    i = j = 0

    while i < len(izq) and j < len(der):
        if izq[i] <= der[j]:
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1

    while i < len(izq):
        resultado.append(izq[i])
        i += 1
    while j < len(der):
        resultado.append(der[j])
        j += 1

    return resultado


# =========================
# ESTRUCTURAS BASE DEL MODELO
# =========================

class Encuestado:
    def __init__(self, id_encuestado, nombre, experticia, opinion):
        self.id = id_encuestado
        self.nombre = nombre
        self.experticia = experticia
        self.opinion = opinion

    def __repr__(self):
        return f"({self.id}, Nombre:'{self.nombre}', Experticia:{self.experticia}, Opinión:{self.opinion})"


class Pregunta:
    def __init__(self, id_pregunta):
        self.id = id_pregunta
        self.encuestados = []

    def agregar_encuestado(self, encuestado):
        self.encuestados.append(encuestado)

    def promedio_opinion(self):
        if not self.encuestados:
            return 0
        return sum(e.opinion for e in self.encuestados) / len(self.encuestados)

    def promedio_experticia(self):
        if not self.encuestados:
            return 0
        return sum(e.experticia for e in self.encuestados) / len(self.encuestados)

    def ordenar_encuestados(self):
        # Insertion Sort manual
        for i in range(1, len(self.encuestados)):
            actual = self.encuestados[i]
            j = i - 1
            while j >= 0 and (
                actual.opinion > self.encuestados[j].opinion or
                (actual.opinion == self.encuestados[j].opinion and actual.experticia > self.encuestados[j].experticia)
            ):
                self.encuestados[j + 1] = self.encuestados[j]
                j -= 1
            self.encuestados[j + 1] = actual

    def mediana_opinion(self):
        opiniones = [e.opinion for e in self.encuestados]
        opiniones = merge_sort(opiniones)
        n = len(opiniones)
        if n == 0:
            return 0
        if n % 2 == 1:
            return opiniones[n // 2]
        else:
            return min(opiniones[n // 2 - 1], opiniones[n // 2])

    def moda_opinion(self):
        if not self.encuestados:
            return 0
        conteo = {}
        for e in self.encuestados:
            conteo[e.opinion] = conteo.get(e.opinion, 0) + 1
        max_frecuencia = max(conteo.values())
        modas = [valor for valor, freq in conteo.items() if freq == max_frecuencia]
        return min(modas)

    def extremismo(self):
        total = len(self.encuestados)
        extremos = sum(1 for e in self.encuestados if e.opinion == 0 or e.opinion == 10)
        return extremos / total if total else 0

    def consenso(self):
        if not self.encuestados:
            return 0
        conteo = {}
        for e in self.encuestados:
            conteo[e.opinion] = conteo.get(e.opinion, 0) + 1
        max_frecuencia = max(conteo.values())
        modas = [valor for valor, freq in conteo.items() if freq == max_frecuencia]
        moda_final = min(modas)
        return conteo[moda_final] / len(self.encuestados)


class Tema:
    def __init__(self, nombre):
        self.nombre = nombre
        self.preguntas = []

    def agregar_pregunta(self, pregunta):
        self.preguntas.append(pregunta)

    def promedio_opiniones(self):
        if not self.preguntas:
            return 0
        return sum(p.promedio_opinion() for p in self.preguntas) / len(self.preguntas)

    def promedio_experticia(self):
        if not self.preguntas:
            return 0
        return sum(p.promedio_experticia() for p in self.preguntas) / len(self.preguntas)

    def total_encuestados(self):
        return sum(len(p.encuestados) for p in self.preguntas)

    def ordenar_preguntas(self):
        # Selection Sort manual
        for i in range(len(self.preguntas)):
            max_idx = i
            for j in range(i + 1, len(self.preguntas)):
                pj = self.preguntas[j]
                pi = self.preguntas[max_idx]
                if (
                    pj.promedio_opinion() > pi.promedio_opinion() or
                    (pj.promedio_opinion() == pi.promedio_opinion() and pj.promedio_experticia() > pi.promedio_experticia()) or
                    (pj.promedio_opinion() == pi.promedio_opinion() and pj.promedio_experticia() == pi.promedio_experticia() and len(pj.encuestados) > len(pi.encuestados))
                ):
                    max_idx = j
            self.preguntas[i], self.preguntas[max_idx] = self.preguntas[max_idx], self.preguntas[i]


class Encuesta:
    def __init__(self):
        self.temas = []
        self.encuestados_dict = {}

    def agregar_tema(self, tema):
        self.temas.append(tema)

    def registrar_encuestado(self, encuestado):
        self.encuestados_dict[encuestado.id] = encuestado

    def ordenar_temas(self):
        # Selection Sort manual
        for i in range(len(self.temas)):
            max_idx = i
            for j in range(i + 1, len(self.temas)):
                tj = self.temas[j]
                ti = self.temas[max_idx]
                if (
                    tj.promedio_opiniones() > ti.promedio_opiniones() or
                    (tj.promedio_opiniones() == ti.promedio_opiniones() and tj.promedio_experticia() > ti.promedio_experticia()) or
                    (tj.promedio_opiniones() == ti.promedio_opiniones() and tj.promedio_experticia() == ti.promedio_experticia() and tj.total_encuestados() > ti.total_encuestados())
                ):
                    max_idx = j
            self.temas[i], self.temas[max_idx] = self.temas[max_idx], self.temas[i]

    def lista_encuestados_ordenada(self):
        encuestados = list(self.encuestados_dict.values())
        for i in range(1, len(encuestados)):
            actual = encuestados[i]
            j = i - 1
            while j >= 0 and (
                actual.experticia > encuestados[j].experticia or
                (actual.experticia == encuestados[j].experticia and actual.id > encuestados[j].id)
            ):
                encuestados[j + 1] = encuestados[j]
                j -= 1
            encuestados[j + 1] = actual
        return encuestados

# =========================
# FUNCIONES DE REPORTE CON DESEMPATE POR ID
# =========================

def obtener_pregunta_mayor_mediana(encuesta):
    mejor = None
    mejor_val = -1
    for tema in encuesta.temas:
        for pregunta in tema.preguntas:
            val = pregunta.mediana_opinion()
            if (val > mejor_val) or (val == mejor_val and (mejor is None or pregunta.id < mejor.id)):
                mejor = pregunta
                mejor_val = val
    return mejor

def obtener_pregunta_menor_mediana(encuesta):
    mejor = None
    mejor_val = 999999
    for tema in encuesta.temas:
        for pregunta in tema.preguntas:
            val = pregunta.mediana_opinion()
            if (val < mejor_val) or (val == mejor_val and (mejor is None or pregunta.id < mejor.id)):
                mejor = pregunta
                mejor_val = val
    return mejor

def obtener_pregunta_mayor_moda(encuesta):
    mejor = None
    mejor_val = -1
    for tema in encuesta.temas:
        for pregunta in tema.preguntas:
            val = pregunta.moda_opinion()
            if (val > mejor_val) or (val == mejor_val and (mejor is None or pregunta.id < mejor.id)):
                mejor = pregunta
                mejor_val = val
    return mejor

def obtener_pregunta_menor_moda(encuesta):
    mejor = None
    mejor_val = 999999
    for tema in encuesta.temas:
        for pregunta in tema.preguntas:
            val = pregunta.moda_opinion()
            if (val < mejor_val) or (val == mejor_val and (mejor is None or pregunta.id < mejor.id)):
                mejor = pregunta
                mejor_val = val
    return mejor

# =========================
# GENERAR ARCHIVO DE SALIDA
# =========================

def generar_salida_txt(encuesta, ruta_salida):
    todas_preguntas = [p for t in encuesta.temas for p in t.preguntas]
    # Mayor promedio experticia
    preg_mayor_exp = max(todas_preguntas, key=lambda p: (p.promedio_experticia(), -float(p.id.replace('.', ''))))
    # Menor promedio experticia
    preg_menor_exp = min(todas_preguntas, key=lambda p: (p.promedio_experticia(), float(p.id.replace('.', ''))))
    preg_mayor_extrem = max(todas_preguntas, key=lambda p: (p.extremismo(), -float(p.id.replace('.', ''))))
    preg_mayor_consenso = max(todas_preguntas, key=lambda p: (p.consenso(), -float(p.id.replace('.', ''))))

    with open(ruta_salida, 'w', encoding='utf-8') as f:
        f.write("Resultados de la encuesta:\n\n")
        for tema in encuesta.temas:
            f.write(f"[{tema.promedio_opiniones():.2f}] {tema.nombre}:\n")
            for pregunta in tema.preguntas:
                ids = ", ".join(str(e.id) for e in pregunta.encuestados)
                f.write(f" [{pregunta.promedio_opinion():.2f}] Pregunta {pregunta.id}: ({ids})\n")
            f.write("\n")

        f.write("Lista de encuestados:\n")
        for e in encuesta.lista_encuestados_ordenada():
            f.write(f" {e}\n")

        # ejemplos de resultados extra
        f.write("\nResultados:\n")
        f.write(f"  Pregunta con mayor promedio de opinion: [{max(p.promedio_opinion() for t in encuesta.temas for p in t.preguntas):.2f}] Pregunta: {max((p for t in encuesta.temas for p in t.preguntas), key=lambda x: x.promedio_opinion()).id}\n")
        f.write(f"  Pregunta con menor promedio de opinion: [{min(p.promedio_opinion() for t in encuesta.temas for p in t.preguntas):.2f}] Pregunta: {min((p for t in encuesta.temas for p in t.preguntas), key=lambda x: x.promedio_opinion()).id}\n")
        f.write(
            f"  Pregunta con mayor promedio de experticia: [{preg_mayor_exp.promedio_experticia():.2f}] Pregunta: {preg_mayor_exp.id}\n")
        f.write(
            f"  Pregunta con menor promedio de experticia: [{preg_menor_exp.promedio_experticia():.2f}] Pregunta: {preg_menor_exp.id}\n")
        f.write(f"  Pregunta con Mayor mediana de opinion: [{obtener_pregunta_mayor_mediana(encuesta).mediana_opinion()}] Pregunta: {obtener_pregunta_mayor_mediana(encuesta).id}\n")
        f.write(f"  Pregunta con menor mediana de opinion: [{obtener_pregunta_menor_mediana(encuesta).mediana_opinion()}] Pregunta: {obtener_pregunta_menor_mediana(encuesta).id}\n")
        f.write(f"  Pregunta con mayor moda de opinion: [{obtener_pregunta_mayor_moda(encuesta).moda_opinion()}] Pregunta: {obtener_pregunta_mayor_moda(encuesta).id}\n")
        f.write(f"  Pregunta con menor moda de opinion: [{obtener_pregunta_menor_moda(encuesta).moda_opinion()}] Pregunta: {obtener_pregunta_menor_moda(encuesta).id}\n")
        f.write(
            f"  Pregunta con mayor extremismo: [{preg_mayor_extrem.extremismo():.2f}] Pregunta: {preg_mayor_extrem.id}\n")
        f.write(
            f"  Pregunta con mayor consenso: [{preg_mayor_consenso.consenso():.2f}] Pregunta: {preg_mayor_consenso.id}\n")
