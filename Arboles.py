"""Calcula y visualiza dos rutas óptimas que recorren siete estados de México.

Modo de ejecución:
    python recorridos_estados.py            # Ventana interactiva
    python recorridos_estados.py --consola  # Resultados y exportación SVG
    python recorridos_estados.py --abrir    # Resultados y apertura del SVG

Las distancias empleadas corresponden a estimaciones geodésicas (línea recta)
entre las capitales estatales y operan de forma bidireccional.
"""

import argparse
from collections import Counter
from heapq import heappop, heappush
from html import escape
from math import asin, cos, radians, sin, sqrt
from pathlib import Path
import webbrowser


# Ubicación geográfica (latitud norte, longitud oeste) de cada capital.
# Referencia: INEGI, Anuario de estadísticas por entidad, cuadro 1.11.
# https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/historicos/2104/702825200794/702825200794_1.pdf
CAPITALES = {
    "Jalisco": (20 + 41 / 60, -(103 + 21 / 60)),      # Guadalajara
    "Michoacán": (19 + 42 / 60, -(101 + 11 / 60)),    # Morelia
    "Guanajuato": (21 + 1 / 60, -(101 + 15 / 60)),    # Guanajuato
    "Querétaro": (20 + 36 / 60, -(100 + 24 / 60)),    # Santiago de Querétaro
    "Hidalgo": (20 + 7 / 60, -(98 + 44 / 60)),        # Pachuca de Soto
    "Puebla": (19 + 3 / 60, -(98 + 12 / 60)),         # Heroica Puebla de Zaragoza
    "Veracruz": (19 + 32 / 60, -(96 + 55 / 60)),      # Xalapa-Enríquez
}


def distancia_km(origen, destino):
    """Calcula la distancia ortodrómica (Haversine) redondeada en kilómetros."""
    lat1, lon1 = map(radians, CAPITALES[origen])
    lat2, lon2 = map(radians, CAPITALES[destino])
    semiverseno = (
        sin((lat2 - lat1) / 2) ** 2
        + cos(lat1) * cos(lat2) * sin((lon2 - lon1) / 2) ** 2
    )
    return round(2 * 6371 * asin(sqrt(semiverseno)))


PARES = (
    ("Jalisco", "Michoacán"),
    ("Jalisco", "Guanajuato"),
    ("Michoacán", "Guanajuato"),
    ("Michoacán", "Querétaro"),
    ("Guanajuato", "Querétaro"),
    ("Querétaro", "Hidalgo"),
    ("Hidalgo", "Puebla"),
    ("Hidalgo", "Veracruz"),
    ("Puebla", "Veracruz"),
)
CONEXIONES = tuple((est_a, est_b, distancia_km(est_a, est_b)) for est_a, est_b in PARES)

# Coordenadas de maquetación para el diagrama (independientes de la geografía).
POSICIONES = {
    "Jalisco": (115, 195),
    "Michoacán": (320, 266),
    "Guanajuato": (320, 124),
    "Querétaro": (525, 195),
    "Hidalgo": (730, 195),
    "Puebla": (935, 124),
    "Veracruz": (935, 266),
}

FUENTE_TEXTO = "Trebuchet MS"
FUENTE_TITULOS = "Georgia"
INTERVALO_REPRODUCCION_MS = 650
ANCHO_NODO = 112
ALTO_NODO = 32

# Paleta de la ventana y del diagrama.
TEMA = {
    "fondo_app": "#faf7f2",
    "fondo_tarjeta": "#ffffff",
    "borde_tarjeta": "#e4ddd3",
    "lienzo": "#f3efe6",
    "texto_principal": "#1c1917",
    "texto_secundario": "#57534e",
    "acento_primario": "#9a3412",      # Terracota oscuro (nodo actual)
    "acento_visitado": "#0f766e",      # Verde azulado / jade (visitado)
    "acento_destino": "#d97706",       # Ámbar dorado (borde de destino)
    "linea_inactiva": "#a8a29e",
    "linea_activa": "#0f766e",
    "etiqueta_fondo": "#fffbeb",
    "etiqueta_borde": "#d6d3d1",
    "nodo_borde": "#a8a29e",
    "visitado_fondo": "#ccfbf1",
    "visitado_texto": "#115e59",
    "tabla_actual_bg": "#ffedd5",
    "tabla_actual_fg": "#9a3412",
}


def construir_grafo(estados, conexiones):
    """Genera el mapa de adyacencia con costos simétricos entre estados."""
    grafo = {estado: {} for estado in estados}
    for origen, destino, costo in conexiones:
        if costo <= 0:
            raise ValueError("Las distancias deben ser positivas.")
        grafo[origen][destino] = costo
        grafo[destino][origen] = costo
    return grafo


def buscar_recorridos(grafo, inicio=None, destino=None):
    """Obtiene los trayectos óptimos (sin repetir y con repetición) mediante Dijkstra."""
    cola_prioridad = []
    costos_minimos = {}
    hallazgos = {False: None, True: None}

    puntos_partida = grafo if inicio is None else (inicio,)
    for punto in puntos_partida:
        visitados = frozenset({punto})
        costos_minimos[punto, visitados, False] = 0
        heappush(cola_prioridad, (0, (punto,), visitados, False))

    while cola_prioridad:
        costo_actual, trayecto, visitados, hubo_repeticion = heappop(cola_prioridad)
        estado_actual = trayecto[-1]

        if costo_actual != costos_minimos[estado_actual, visitados, hubo_repeticion]:
            continue

        en_meta = destino is None or estado_actual == destino
        if en_meta and len(visitados) == len(grafo) and hallazgos[hubo_repeticion] is None:
            hallazgos[hubo_repeticion] = (trayecto, costo_actual)
            if all(hallazgos.values()):
                break

        for vecino, distancia in grafo[estado_actual].items():
            nuevos_visitados = visitados | {vecino}
            repite = hubo_repeticion or (vecino in visitados)
            estado_busqueda = (vecino, nuevos_visitados, repite)
            costo_acumulado = costo_actual + distancia

            if costo_acumulado < costos_minimos.get(estado_busqueda, float("inf")):
                costos_minimos[estado_busqueda] = costo_acumulado
                heappush(
                    cola_prioridad,
                    (costo_acumulado, trayecto + (vecino,), nuevos_visitados, repite),
                )

    return hallazgos[False], hallazgos[True]


def mostrar_recorrido(titulo, resultado, grafo):
    """Imprime en consola el desglose formateado de un recorrido."""
    barra = "─" * len(titulo)
    print(f"\n┌─{barra}─┐")
    print(f"│ {titulo} │")
    print(f"└─{barra}─┘")

    if resultado is None:
        print("  ✗ No existe un recorrido que cumpla esta condición.")
        return

    ruta, costo = resultado
    tramos = [str(grafo[a][b]) for a, b in zip(ruta, ruta[1:])]
    repetidos = [
        f"{estado} ({veces} veces)"
        for estado, veces in Counter(ruta).items()
        if veces > 1
    ]

    print(f"  ▸ Ruta:              {' ➔ '.join(ruta)}")
    print(f"  ▸ Distancia total:   {' + '.join(tramos)} = {costo:,} km")
    print(f"  ▸ Estados repetidos: {', '.join(repetidos) or 'ninguno'}")


def dibujar_grafo(conexiones, posiciones, archivo):
    """Exporta una representación vectorial (SVG) estilizada del grafo."""
    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1050 350" width="1050" height="350" role="img" aria-labelledby="titulo detalle">',
        '<title id="titulo">Grafo de siete estados de México</title>',
        '<desc id="detalle">Conexiones bidireccionales con distancias aproximadas en línea recta entre capitales.</desc>',
        '<defs>',
        '  <linearGradient id="fondoGrad" x1="0%" y1="0%" x2="100%" y2="100%">',
        '    <stop offset="0%" stop-color="#faf7f2"/>',
        '    <stop offset="100%" stop-color="#f0eae1"/>',
        '  </linearGradient>',
        '  <filter id="sombra" x="-10%" y="-10%" width="125%" height="130%">',
        '    <feDropShadow dx="0" dy="3" stdDeviation="3" flood-color="#1c1917" flood-opacity="0.14"/>',
        '  </filter>',
        '</defs>',
        '<rect width="1050" height="350" rx="20" fill="url(#fondoGrad)" stroke="#e4ddd3" stroke-width="2"/>',
        '<g font-family="Georgia, \'Times New Roman\', serif">',
        '<text x="42" y="48" font-size="26" font-weight="700" fill="#1c1917">Red carretera esquemática · Siete estados de México</text>',
        '</g>',
        '<g font-family="\'Trebuchet MS\', Helvetica, sans-serif">',
        '<text x="42" y="74" font-size="14" fill="#57534e">Conexiones en ambos sentidos · Distancias geodésicas aproximadas entre capitales (km)</text>',
    ]

    etiquetas = []
    for origen, destino, costo in conexiones:
        x1, y1 = posiciones[origen]
        x2, y2 = posiciones[destino]
        svg.append(
            f'<line x1="{x1}" y1="{y1 + 8}" x2="{x2}" y2="{y2 + 8}" '
            'stroke="#a8a29e" stroke-width="3" stroke-linecap="round" stroke-dasharray="6,3"/>'
        )
        xm, ym = (x1 + x2) / 2, (y1 + y2) / 2 + 8
        etiquetas.append(
            f'<rect x="{xm - 36}" y="{ym - 13}" width="72" height="26" rx="13" '
            'fill="#fffbeb" stroke="#d97706" stroke-width="1.2" filter="url(#sombra)"/>'
        )
        etiquetas.append(
            f'<text x="{xm}" y="{ym + 5}" text-anchor="middle" font-size="13" '
            f'font-weight="700" fill="#78350f">{costo} km</text>'
        )

    # Las etiquetas se dibujan encima de todas las conexiones.
    svg.extend(etiquetas)

    for estado, (x, y) in posiciones.items():
        cy = y + 8
        svg.append(
            f'<rect x="{x - ANCHO_NODO / 2}" y="{cy - ALTO_NODO / 2}" '
            f'width="{ANCHO_NODO}" height="{ALTO_NODO}" rx="{ALTO_NODO / 2}" '
            f'fill="{TEMA["fondo_tarjeta"]}" stroke="{TEMA["nodo_borde"]}"/>'
        )
        svg.append(
            f'<text x="{x}" y="{cy}" text-anchor="middle" dominant-baseline="central" '
            f'font-size="14" font-weight="700" fill="{TEMA["texto_principal"]}">{escape(estado)}</text>'
        )

    svg.append("</g></svg>")
    archivo.write_text("\n".join(svg) + "\n", encoding="utf-8")


def mostrar_consola(grafo, abrir):
    """Despliega el informe completo en la terminal y genera el archivo SVG."""
    print("═" * 78)
    print("  GRAFO DE ESTADOS · CONEXIONES Y DISTANCIAS EN LÍNEA RECTA ENTRE CAPITALES")
    print("═" * 78)
    for estado, vecinos in grafo.items():
        relaciones = ", ".join(f"{vecino} ({costo} km)" for vecino, costo in vecinos.items())
        print(f"  • {estado:<11} ➔  {relaciones}")

    sin_repetir, con_repeticion = buscar_recorridos(grafo)
    mostrar_recorrido("A) Visitar los siete estados sin repetir", sin_repetir, grafo)
    mostrar_recorrido("B) Visitar los siete estados repitiendo al menos uno", con_repeticion, grafo)

    archivo = Path(__file__).with_name("grafo_estados.svg").resolve()
    dibujar_grafo(CONEXIONES, POSICIONES, archivo)
    print(f"\n[✓] Diagrama SVG generado en: {archivo}")
    if abrir and not webbrowser.open(archivo.as_uri()):
        print("    Abre el archivo SVG manualmente en tu navegador.")


def abrir_ventana(grafo):
    """Inicializa la ventana interactiva de simulación en Tkinter."""
    import tkinter as tk
    from tkinter import ttk

    raiz = tk.Tk()
    raiz.title("Atlas Interactivo · Recorridos por Siete Estados de México")
    raiz.geometry("1040x770")
    raiz.minsize(800, 620)
    raiz.configure(bg=TEMA["fondo_app"])
    Simulador(raiz, grafo, tk, ttk)
    raiz.mainloop()


class Simulador:
    """Interfaz gráfica para explorar paso a paso las rutas y su árbol de decisión."""

    def __init__(self, raiz, grafo, tk, ttk):
        self.raiz = raiz
        self.grafo = grafo
        self.inicio = tk.StringVar(value="Michoacán")
        self.destino = tk.StringVar(value="Veracruz")
        self.modo = tk.IntVar(value=0)
        self.resumen = tk.StringVar()
        self.detalle = tk.StringVar()
        self.temporizador = None
        self.paso = 0
        self.ruta = ()

        self._configurar_estilos(ttk)
        self._construir_interfaz(tk, ttk)

        raiz.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.cambiar_extremos()

    def _configurar_estilos(self, ttk):
        estilo = ttk.Style(self.raiz)
        if "clam" in estilo.theme_names():
            estilo.theme_use("clam")

        estilo.configure("Fondo.TFrame", background=TEMA["fondo_app"])
        estilo.configure(
            "Tarjeta.TFrame",
            background=TEMA["fondo_tarjeta"],
            relief="solid",
            borderwidth=1,
        )
        estilo.configure(
            "Titulo.TLabel",
            background=TEMA["fondo_app"],
            foreground=TEMA["texto_principal"],
            font=(FUENTE_TITULOS, 20, "bold"),
        )
        estilo.configure(
            "Subtitulo.TLabel",
            background=TEMA["fondo_app"],
            foreground=TEMA["texto_secundario"],
            font=(FUENTE_TEXTO, 10),
        )
        estilo.configure(
            "Seccion.TLabel",
            background=TEMA["fondo_app"],
            foreground=TEMA["texto_principal"],
            font=(FUENTE_TITULOS, 13, "bold"),
        )
        estilo.configure(
            "EtiquetaBarra.TLabel",
            background=TEMA["fondo_tarjeta"],
            foreground=TEMA["texto_principal"],
            font=(FUENTE_TEXTO, 10, "bold"),
        )
        estilo.configure(
            "Resumen.TLabel",
            background=TEMA["fondo_tarjeta"],
            foreground=TEMA["acento_primario"],
            font=(FUENTE_TEXTO, 11, "bold"),
        )
        estilo.configure(
            "Detalle.TLabel",
            background=TEMA["fondo_tarjeta"],
            foreground=TEMA["texto_secundario"],
            font=(FUENTE_TEXTO, 10),
        )
        estilo.configure(
            "Leyenda.TLabel",
            background=TEMA["fondo_app"],
            foreground=TEMA["texto_secundario"],
            font=(FUENTE_TEXTO, 9),
        )
        estilo.configure(
            "Modo.TRadiobutton",
            background=TEMA["fondo_tarjeta"],
            foreground=TEMA["texto_principal"],
            font=(FUENTE_TEXTO, 10),
        )
        estilo.configure(
            "Control.TButton",
            font=(FUENTE_TEXTO, 10, "bold"),
            padding=(12, 5),
        )
        estilo.configure(
            "Treeview",
            background=TEMA["fondo_tarjeta"],
            fieldbackground=TEMA["fondo_tarjeta"],
            foreground=TEMA["texto_principal"],
            rowheight=26,
            font=(FUENTE_TEXTO, 10),
        )
        estilo.configure(
            "Treeview.Heading",
            background="#e7e0d6",
            foreground=TEMA["texto_principal"],
            font=(FUENTE_TEXTO, 10, "bold"),
        )

    def _construir_interfaz(self, tk, ttk):
        contenedor = ttk.Frame(self.raiz, padding=18, style="Fondo.TFrame")
        contenedor.pack(fill="both", expand=True)

        # Encabezado
        ttk.Label(
            contenedor,
            text="Atlas de Recorridos Mínimos por México",
            style="Titulo.TLabel",
        ).pack(anchor="w")
        ttk.Label(
            contenedor,
            text="Selecciona los estados de partida y llegada. Los costos representan distancias geodésicas aproximadas entre capitales.",
            style="Subtitulo.TLabel",
        ).pack(anchor="w", pady=(2, 10))

        # Barra superior de configuración en tarjeta
        barra_config = ttk.Frame(contenedor, padding=(14, 10), style="Tarjeta.TFrame")
        barra_config.pack(fill="x", pady=(0, 10))

        for etiqueta, variable in (("Origen:", self.inicio), ("Meta:", self.destino)):
            ttk.Label(barra_config, text=etiqueta, style="EtiquetaBarra.TLabel").pack(side="left")
            selector = ttk.Combobox(
                barra_config,
                textvariable=variable,
                values=tuple(self.grafo),
                state="readonly",
                width=14,
                font=(FUENTE_TEXTO, 10),
            )
            selector.pack(side="left", padx=(6, 18))
            selector.bind("<<ComboboxSelected>>", self.cambiar_extremos)

        ttk.Label(barra_config, text="Modalidad:", style="EtiquetaBarra.TLabel").pack(
            side="left", padx=(6, 8)
        )
        for indice, titulo in enumerate(("A · Sin repetir estado", "B · Repitiendo al menos uno")):
            ttk.Radiobutton(
                barra_config,
                text=titulo,
                variable=self.modo,
                value=indice,
                command=self.cargar_ruta,
                style="Modo.TRadiobutton",
            ).pack(side="left", padx=(0, 14))

        # Lienzo interactivo del mapa esquemático
        marco_lienzo = tk.Frame(
            contenedor,
            bg=TEMA["borde_tarjeta"],
            bd=1,
            relief="solid",
        )
        marco_lienzo.pack(fill="x", pady=(2, 4))
        self.lienzo = tk.Canvas(
            marco_lienzo,
            height=215,
            background=TEMA["lienzo"],
            highlightthickness=0,
        )
        self.lienzo.pack(fill="x")
        self.lienzo.bind("<Configure>", self.dibujar)

        ttk.Label(
            contenedor,
            text="● Jade claro: visitado    ● Terracota: estado actual    → Último tramo    ◯ Borde ámbar: meta",
            style="Leyenda.TLabel",
        ).pack(anchor="w", pady=(2, 8))

        # Panel de reproducción y estado actual
        panel_estado = ttk.Frame(contenedor, padding=(14, 10), style="Tarjeta.TFrame")
        panel_estado.pack(fill="x", pady=(0, 12))

        controles = ttk.Frame(panel_estado, style="Tarjeta.TFrame")
        controles.pack(side="left", padx=(0, 18))

        def crear_boton(texto, comando):
            boton = ttk.Button(controles, text=texto, style="Control.TButton", command=comando)
            boton.pack(side="left", padx=(0, 6))
            return boton

        self.reiniciar = crear_boton("⏮ Reiniciar", lambda: self.mover(-self.paso))
        self.anterior = crear_boton("◀ Anterior", lambda: self.mover(-1))
        self.siguiente = crear_boton("Siguiente ▶", lambda: self.mover(1))
        self.reproducir = crear_boton("▶ Reproducir", self.alternar_reproduccion)

        textos_estado = ttk.Frame(panel_estado, style="Tarjeta.TFrame")
        textos_estado.pack(side="left", fill="x", expand=True)
        ttk.Label(textos_estado, textvariable=self.resumen, style="Resumen.TLabel").pack(anchor="w")
        ttk.Label(textos_estado, textvariable=self.detalle, style="Detalle.TLabel").pack(
            anchor="w", pady=(2, 0)
        )

        # Sección del árbol comparativo
        ttk.Label(
            contenedor,
            text="Árbol comparativo de trayectorias",
            style="Seccion.TLabel",
        ).pack(anchor="w")
        ttk.Label(
            contenedor,
            text="Los prefijos idénticos se agrupan en una misma rama. El símbolo ↻ señala que el estado ya había sido visitado.",
            style="Leyenda.TLabel",
        ).pack(anchor="w", pady=(0, 4))

        marco_arbol = ttk.Frame(contenedor, style="Tarjeta.TFrame")
        marco_arbol.pack(fill="both", expand=True)

        self.arbol = ttk.Treeview(
            marco_arbol,
            columns=("tramo", "acumulado", "caso"),
            selectmode="none",
            height=8,
        )
        self.arbol.heading("#0", text="Secuencia de estados")
        self.arbol.column("#0", width=370, minwidth=240)
        for clave, titulo, ancho in (
            ("tramo", "Tramo actual", 135),
            ("acumulado", "Distancia acumulada", 155),
            ("caso", "Modalidad", 120),
        ):
            self.arbol.heading(clave, text=titulo)
            self.arbol.column(clave, width=ancho, stretch=False, anchor="center")

        barra = ttk.Scrollbar(marco_arbol, orient="vertical", command=self.arbol.yview)
        self.arbol.configure(yscrollcommand=barra.set)
        self.arbol.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

        self.arbol.tag_configure(
            "visitado",
            background=TEMA["visitado_fondo"],
            foreground=TEMA["visitado_texto"],
        )
        self.arbol.tag_configure(
            "actual",
            background=TEMA["tabla_actual_bg"],
            foreground=TEMA["tabla_actual_fg"],
        )

    def cambiar_extremos(self, _evento=None):
        inicio = self.inicio.get()
        self.resultados = buscar_recorridos(self.grafo, inicio, self.destino.get())
        self.arbol.delete(*self.arbol.get_children())
        nodo_raiz = self.arbol.insert(
            "", "end", text=inicio, values=("—", "0 km", ""), open=True
        )
        self.nodos = {(inicio,): nodo_raiz}

        for etiqueta_caso, resultado in zip(("A", "B"), self.resultados):
            if resultado is None:
                continue
            ruta, _ = resultado
            acumulado = 0
            for indice_paso, (origen, destino) in enumerate(zip(ruta, ruta[1:]), start=1):
                tramo = self.grafo[origen][destino]
                acumulado += tramo
                prefijo = ruta[: indice_paso + 1]
                if prefijo not in self.nodos:
                    nombre = f"{destino} ↻" if destino in prefijo[:-1] else destino
                    self.nodos[prefijo] = self.arbol.insert(
                        self.nodos[prefijo[:-1]],
                        "end",
                        text=nombre,
                        values=(f"{tramo:,} km", f"{acumulado:,} km", ""),
                        open=True,
                    )
            self.arbol.set(self.nodos[ruta], "caso", etiqueta_caso)

        self.cargar_ruta()

    def cargar_ruta(self):
        self.pausar()
        self.resultado = self.resultados[self.modo.get()]
        self.ruta = self.resultado[0] if self.resultado else (self.inicio.get(),)
        self.paso = 0
        self.actualizar()

    def mover(self, cantidad):
        self.pausar()
        self.paso = max(0, min(self.paso + cantidad, len(self.ruta) - 1))
        self.actualizar()

    def pausar(self):
        if self.temporizador is not None:
            self.raiz.after_cancel(self.temporizador)
            self.temporizador = None
        self.reproducir.configure(text="▶ Reproducir")

    def alternar_reproduccion(self):
        if self.temporizador is not None:
            self.pausar()
            return
        if self.paso == len(self.ruta) - 1:
            self.paso = 0
            self.actualizar()
        self.reproducir.configure(text="⏸ Pausar")
        self.temporizador = self.raiz.after(INTERVALO_REPRODUCCION_MS, self.avanzar)

    def avanzar(self):
        self.temporizador = None
        self.paso += 1
        self.actualizar()
        if self.paso < len(self.ruta) - 1:
            self.temporizador = self.raiz.after(INTERVALO_REPRODUCCION_MS, self.avanzar)
        else:
            self.pausar()

    def cerrar(self):
        self.pausar()
        self.raiz.destroy()

    def actualizar(self):
        prefijo = self.ruta[: self.paso + 1]
        actual = prefijo[-1]
        for ruta, nodo in self.nodos.items():
            etiquetas = ()
            if ruta == prefijo:
                etiquetas = ("actual",)
            elif prefijo[: len(ruta)] == ruta:
                etiquetas = ("visitado",)
            self.arbol.item(nodo, tags=etiquetas)
        self.arbol.see(self.nodos[prefijo])

        if self.resultado:
            tramos = [self.grafo[a][b] for a, b in zip(prefijo, prefijo[1:])]
            self.resumen.set(
                f"Tramos recorridos: {self.paso}/{len(self.ruta) - 1}   │   "
                f"Estados cubiertos: {len(set(prefijo))}/{len(self.grafo)}   │   "
                f"Distancia acumulada: {sum(tramos):,} km de {self.resultado[1]:,} km"
            )
            if tramos:
                nota = " · Visita repetida" if actual in prefijo[:-1] else ""
                if self.paso == len(self.ruta) - 1:
                    nota += " · ¡Meta completada!"
                self.detalle.set(f"Último movimiento: {prefijo[-2]} ➔ {actual}  (+{tramos[-1]:,} km){nota}")
            else:
                self.detalle.set(f"Punto de partida fijado en {actual}. Usa «Siguiente» o «Reproducir» para iniciar.")
        else:
            self.resumen.set(f"Sin solución disponible para ir de {actual} a {self.destino.get()} en esta modalidad.")
            self.detalle.set("Selecciona otra combinación de origen, meta o modalidad de recorrido.")

        self.reiniciar.configure(state="normal" if self.paso else "disabled")
        self.anterior.configure(state="normal" if self.paso else "disabled")
        self.siguiente.configure(state="normal" if self.paso < len(self.ruta) - 1 else "disabled")
        self.reproducir.configure(state="normal" if self.resultado else "disabled")
        self.dibujar()

    def dibujar(self, _evento=None):
        ancho = self.lienzo.winfo_width()
        if ancho < 200 or not self.ruta:
            return
        self.lienzo.delete("all")

        posiciones = {
            estado: (x * ancho / 1050, y - 88)
            for estado, (x, y) in POSICIONES.items()
        }
        visitados = self.ruta[: self.paso + 1]
        cantidades = Counter(visitados)
        traslados = {frozenset((a, b)) for a, b in zip(visitados, visitados[1:])}

        # Dibujo de aristas
        for origen, destino, _ in CONEXIONES:
            marcado = frozenset((origen, destino)) in traslados
            self.lienzo.create_line(
                *posiciones[origen],
                *posiciones[destino],
                fill=TEMA["linea_activa"] if marcado else TEMA["linea_inactiva"],
                width=4 if marcado else 2,
                dash=() if marcado else (5, 3),
            )

        # Flecha indicadora del último traslado
        if self.paso:
            x1, y1 = posiciones[visitados[-2]]
            x2, y2 = posiciones[visitados[-1]]
            dx, dy = x2 - x1, y2 - y1
            self.lienzo.create_line(
                x1 + dx * 0.38,
                y1 + dy * 0.38,
                x1 + dx * 0.58,
                y1 + dy * 0.58,
                fill=TEMA["acento_primario"],
                width=4,
                arrow="last",
                arrowshape=(11, 14, 6),
            )

        # Etiquetas de kilometraje en cada conexión
        for origen, destino, costo in CONEXIONES:
            x1, y1 = posiciones[origen]
            x2, y2 = posiciones[destino]
            xm, ym = (x1 + x2) / 2, (y1 + y2) / 2
            if x1 == x2:
                xm += 36
            else:
                ym += 19 if ym > 106 else -19
            self.lienzo.create_rectangle(
                xm - 30,
                ym - 10,
                xm + 30,
                ym + 10,
                fill=TEMA["etiqueta_fondo"],
                outline=TEMA["etiqueta_borde"],
            )
            self.lienzo.create_text(
                xm,
                ym,
                text=f"{costo} km",
                fill=TEMA["texto_principal"],
                font=(FUENTE_TEXTO, 9, "bold"),
            )

        actual = visitados[-1]
        destino = self.destino.get()
        # Dibujo de nodos de los estados
        for estado, (x, y) in posiciones.items():
            if estado == actual:
                fondo = borde = TEMA["acento_primario"]
                texto = TEMA["fondo_tarjeta"]
            elif estado in cantidades:
                fondo = TEMA["visitado_fondo"]
                borde = TEMA["acento_visitado"]
                texto = TEMA["visitado_texto"]
            else:
                fondo = TEMA["fondo_tarjeta"]
                borde = TEMA["nodo_borde"]
                texto = TEMA["texto_principal"]

            es_destino = estado == destino
            radio = ALTO_NODO / 2
            izquierda, derecha = x - ANCHO_NODO / 2, x + ANCHO_NODO / 2
            arriba, abajo = y - radio, y + radio
            self.lienzo.create_polygon(
                (izquierda + radio, arriba),
                (derecha - radio, arriba),
                (derecha, arriba),
                (derecha, y),
                (derecha, abajo),
                (derecha - radio, abajo),
                (izquierda + radio, abajo),
                (izquierda, abajo),
                (izquierda, y),
                (izquierda, arriba),
                smooth=True,
                fill=fondo,
                outline=TEMA["acento_destino"] if es_destino else borde,
                width=3 if es_destino else 1,
            )
            self.lienzo.create_text(
                x,
                y,
                text=estado,
                fill=texto,
                font=(FUENTE_TEXTO, -14, "bold"),
            )
            if cantidades[estado] > 1:
                self.lienzo.create_text(
                    x,
                    y + 27,
                    text=f"↻ {cantidades[estado]} visitas",
                    fill=TEMA["acento_primario"],
                    font=(FUENTE_TEXTO, 9, "bold"),
                )


def main():
    selector_cli = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    grupo_modo = selector_cli.add_mutually_exclusive_group()
    grupo_modo.add_argument(
        "--consola",
        action="store_true",
        help="Muestra los resultados en la terminal.",
    )
    grupo_modo.add_argument(
        "--abrir",
        action="store_true",
        help="Muestra los resultados en la terminal y abre el SVG.",
    )
    argumentos = selector_cli.parse_args()
    grafo = construir_grafo(CAPITALES, CONEXIONES)

    if argumentos.consola or argumentos.abrir:
        mostrar_consola(grafo, argumentos.abrir)
    else:
        abrir_ventana(grafo)


if __name__ == "__main__":
    main()
