# =============================
# ESTRATEGIA 2 - Árboles Binarios de Búsqueda
# =============================

# ---------- Clase base de encuestado ----------
class Encuestado:
    def __init__(self, id_encuestado, nombre, experticia, opinion):
        self.id = id_encuestado
        self.nombre = nombre
        self.experticia = experticia
        self.opinion = opinion

    def __repr__(self):
        return f"({self.id}, {self.opinion})"

# ---------- Nodo y ABB de encuestados ----------
class NodoEncuestado:
    def __init__(self, encuestado):
        self.encuestado = encuestado
        self.izq = None
        self.der = None

class ABBEncuestados:
    def __init__(self):
        self.raiz = None

    def insertar(self, encuestado):
        self.raiz = self._insertar(self.raiz, encuestado)

    def _insertar(self, nodo, encuestado):
        if nodo is None:
            return NodoEncuestado(encuestado)
        # orden descendente por opinion, luego experticia
        if (encuestado.opinion > nodo.encuestado.opinion) or \
           (encuestado.opinion == nodo.encuestado.opinion and encuestado.experticia > nodo.encuestado.experticia):
            nodo.izq = self._insertar(nodo.izq, encuestado)
        else:
            nodo.der = self._insertar(nodo.der, encuestado)
        return nodo

    def inorder(self):
        resultado = []
        self._inorder(self.raiz, resultado)
        return resultado

    def _inorder(self, nodo, resultado):
        if nodo:
            self._inorder(nodo.izq, resultado)
            resultado.append(nodo.encuestado)
            self._inorder(nodo.der, resultado)

# ---------- Pregunta usando ABB ----------
class PreguntaHeap:
    def __init__(self, nombre):
        self.nombre = nombre
        self.encuestados_abb = ABBEncuestados()
        self.encuestados_lista = []  # para cálculos estadísticos fáciles

    def agregar_encuestado(self, encuestado):
        self.encuestados_abb.insertar(encuestado)
        self.encuestados_lista.append(encuestado)

    def lista_encuestados(self):
        return self.encuestados_abb.inorder()

    def promedio_opinion(self):
        if not self.encuestados_lista:
            return 0
        return sum(e.opinion for e in self.encuestados_lista) / len(self.encuestados_lista)

    def promedio_experticia(self):
        if not self.encuestados_lista:
            return 0
        return sum(e.experticia for e in self.encuestados_lista) / len(self.encuestados_lista)

    def mediana_opinion(self):
        n = len(self.encuestados_lista)
        if n == 0:
            return 0
        valores = sorted([e.opinion for e in self.encuestados_lista])
        if n % 2 == 1:
            return valores[n//2]
        else:
            return min(valores[n//2-1], valores[n//2])  # menor valor si par

    def moda_opinion(self):
        if not self.encuestados_lista:
            return 0
        conteo = {}
        for e in self.encuestados_lista:
            conteo[e.opinion] = conteo.get(e.opinion, 0) + 1
        max_f = max(conteo.values())
        modas = [v for v, f in conteo.items() if f == max_f]
        return min(modas)  # menor valor en caso de empate

    def extremismo(self):
        n = len(self.encuestados_lista)
        if n == 0:
            return 0
        extremos = sum(1 for e in self.encuestados_lista if e.opinion == 0 or e.opinion == 10)
        return extremos / n

    def consenso(self):
        if not self.encuestados_lista:
            return 0
        conteo = {}
        for e in self.encuestados_lista:
            conteo[e.opinion] = conteo.get(e.opinion, 0) + 1
        max_f = max(conteo.values())
        modas = [v for v, f in conteo.items() if f == max_f]
        moda_final = min(modas)
        return conteo[moda_final] / len(self.encuestados_lista)

# ---------- Nodo y ABB de preguntas ----------
class NodoPregunta:
    def __init__(self, pregunta):
        self.pregunta = pregunta
        self.izq = None
        self.der = None

class TemaABB:
    def __init__(self, nombre):
        self.nombre = nombre
        self.raiz = None
        self.preguntas = []

    def agregar_pregunta(self, pregunta):
        self.preguntas.append(pregunta)
        self.raiz = self._insertar(self.raiz, pregunta)

    def _insertar(self, nodo, pregunta):
        if nodo is None:
            return NodoPregunta(pregunta)
        # criterio descendente por promedio opinion, luego experticia
        if (pregunta.promedio_opinion() > nodo.pregunta.promedio_opinion()) or \
           (pregunta.promedio_opinion() == nodo.pregunta.promedio_opinion() and pregunta.promedio_experticia() > nodo.pregunta.promedio_experticia()):
            nodo.izq = self._insertar(nodo.izq, pregunta)
        else:
            nodo.der = self._insertar(nodo.der, pregunta)
        return nodo

    def preguntas_ordenadas(self):
        resultado = []
        self._inorder(self.raiz, resultado)
        return resultado

    def _inorder(self, nodo, resultado):
        if nodo:
            self._inorder(nodo.izq, resultado)
            resultado.append(nodo.pregunta)
            self._inorder(nodo.der, resultado)

    def promedio_opiniones(self):
        if not self.preguntas:
            return 0
        return sum(p.promedio_opinion() for p in self.preguntas) / len(self.preguntas)

    def promedio_experticia(self):
        if not self.preguntas:
            return 0
        return sum(p.promedio_experticia() for p in self.preguntas) / len(self.preguntas)

    def total_encuestados(self):
        return sum(len(p.encuestados_lista) for p in self.preguntas)

# ---------- Nodo y ABB de temas ----------
class NodoTema:
    def __init__(self, tema):
        self.tema = tema
        self.izq = None
        self.der = None

class EncuestaHeapABB:
    def __init__(self):
        self.raiz = None
        self.encuestados = {}

    def registrar_encuestado(self, encuestado):
        self.encuestados[encuestado.id] = encuestado

    def agregar_tema(self, tema):
        self.raiz = self._insertar(self.raiz, tema)

    def _insertar(self, nodo, tema):
        if nodo is None:
            return NodoTema(tema)
        if (tema.promedio_opiniones() > nodo.tema.promedio_opiniones()) or \
           (tema.promedio_opiniones() == nodo.tema.promedio_opiniones() and tema.promedio_experticia() > nodo.tema.promedio_experticia()):
            nodo.izq = self._insertar(nodo.izq, tema)
        else:
            nodo.der = self._insertar(nodo.der, tema)
        return nodo

    def temas_ordenados(self):
        resultado = []
        self._inorder(self.raiz, resultado)
        return resultado

    def _inorder(self, nodo, resultado):
        if nodo:
            self._inorder(nodo.izq, resultado)
            resultado.append(nodo.tema)
            self._inorder(nodo.der, resultado)

# =============================
# FUNCIONES GLOBALES DE REPORTE
# =============================

def obtener_pregunta_mayor_mediana(encuesta):
    mejor = None
    mejor_valor = -1
    for tema in encuesta.temas_ordenados():
        for pregunta in tema.preguntas_ordenadas():
            val = pregunta.mediana_opinion()
            if (val > mejor_valor) or (val == mejor_valor and (mejor is None or pregunta.nombre < mejor.nombre)):
                mejor = pregunta
                mejor_valor = val
    return mejor

def obtener_pregunta_menor_mediana(encuesta):
    mejor = None
    mejor_valor = 999999
    for tema in encuesta.temas_ordenados():
        for pregunta in tema.preguntas_ordenadas():
            val = pregunta.mediana_opinion()
            if (val < mejor_valor) or (val == mejor_valor and (mejor is None or pregunta.nombre < mejor.nombre)):
                mejor = pregunta
                mejor_valor = val
    return mejor

def obtener_pregunta_mayor_moda(encuesta):
    mejor = None
    mejor_valor = -1
    for tema in encuesta.temas_ordenados():
        for pregunta in tema.preguntas_ordenadas():
            val = pregunta.moda_opinion()
            if (val > mejor_valor) or (val == mejor_valor and (mejor is None or pregunta.nombre < mejor.nombre)):
                mejor = pregunta
                mejor_valor = val
    return mejor

def obtener_pregunta_menor_moda(encuesta):
    mejor = None
    mejor_valor = 999999
    for tema in encuesta.temas_ordenados():
        for pregunta in tema.preguntas_ordenadas():
            val = pregunta.moda_opinion()
            if (val < mejor_valor) or (val == mejor_valor and (mejor is None or pregunta.nombre < mejor.nombre)):
                mejor = pregunta
                mejor_valor = val
    return mejor

# =============================
# GENERAR ARCHIVO DE SALIDA
# =============================
def generar_salida_txt_estrategia2(encuesta, ruta_salida):
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        for tema in encuesta.temas_ordenados():
            f.write(f"[{tema.promedio_opiniones():.2f}] {tema.nombre}\n")
            for pregunta in tema.preguntas_ordenadas():
                ids_enc = " ".join(str(e.id) for e in pregunta.lista_encuestados())
                f.write(f"[{pregunta.promedio_opinion():.2f}] Pregunta {pregunta.nombre}: ({ids_enc})\n")
        # lista global de encuestados
        f.write("Lista de encuestados:\n")
        # Ordenar encuestados globales por experticia desc, luego id desc (insertion sort manual)
        encuestados = list(encuesta.encuestados.values())
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
        f.write(" ".join(str(e.id) for e in encuestados))
