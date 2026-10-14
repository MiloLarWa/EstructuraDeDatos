import tkinter as tk
from tkinter import messagebox

class TorreDeHanoiInteractivo:
    def __init__(self, root):
        self.root = root
        self.root.title("Torre de Hanói Interactiva")
        self.root.geometry("900x620")
        self.root.configure(bg="#f4f4d7")

        # Variables de estado del juego
        self.num_discos = 13  # Valor inicial igual que en la imagen
        self.movimientos = 0
        self.torres = [[], [], []]
        
        # Variables para arrastrar y soltar (Drag & Drop) o clic
        self.torre_seleccionada = None
        self.disco_arrastrado = None
        self.torre_origen_arrastre = None
        self.auto_resolviendo = False
        self.after_id = None

        # Lienzo principal (Canvas)
        self.canvas = tk.Canvas(
            self.root, width=900, height=620, 
            bg="#f4f4d7", highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        # Coordenadas geométricas del tablero
        self. postes_x = [260, 460, 660]
        self.base_y = 500
        self.poste_top_y = 220

        # Vinculación de eventos del ratón
        self.canvas.bind("<ButtonPress-1>", self.al_presionar_raton)
        self.canvas.bind("<B1-Motion>", self.al_arrastrar_raton)
        self.canvas.bind("<ButtonRelease-1>", self.al_soltar_raton)

        self.reiniciar_juego()

    def reiniciar_juego(self):
        """Reinicia las torres, el contador de movimientos y detiene animaciones."""
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.auto_resolviendo = False
        self.movimientos = 0
        self.torre_seleccionada = None
        self.disco_arrastrado = None
        
        # Llenar la primera torre con discos del más grande (n) al más pequeño (1)
        self.torres = [list(range(self.num_discos, 0, -1)), [], []]
        self.dibujar_escena()

    def dibujar_rectangulo_redondeado(self, x1, y1, x2, y2, radio=8, **kwargs):
        """Dibuja un rectángulo con esquinas redondeadas en el Canvas."""
        puntos = [
            x1 + radio, y1,
            x2 - radio, y1,
            x2, y1,
            x2, y1 + radio,
            x2, y2 - radio,
            x2, y2,
            x2 - radio, y2,
            x1 + radio, y2,
            x1, y2,
            x1, y2 - radio,
            x1, y1 + radio,
            x1, y1
        ]
        return self.canvas.create_polygon(puntos, smooth=True, **kwargs)

    def dibujar_escena(self):
        """Renderiza toda la interfaz gráfica idéntica a la imagen de referencia."""
        self.canvas.delete("all")

        # 1. Dibujar el Slider personalizado (parte superior central)
        slider_x1, slider_x2, slider_y = 370, 530, 85
        self.canvas.create_line(
            slider_x1, slider_y, slider_x2, slider_y, 
            fill="#6e7065", width=5, capstyle="round"
        )
        
        # Posición de la perilla según el número de discos (rango de 1 a 13)
        proporcion = (self.num_discos - 1) / 12.0
        knob_x = slider_x1 + proporcion * (slider_x2 - slider_x1)
        
        # Texto del número de discos arriba de la perilla
        self.canvas.create_text(
            knob_x, slider_y - 22, text=str(self.num_discos),
            font=("Georgia", 12, "bold"), fill="#555555"
        )
        # Perilla circular doble
        self.canvas.create_oval(
            knob_x - 13, slider_y - 13, knob_x + 13, slider_y + 13,
            fill="#7a7c70", outline="#2e302a", width=2, tags="slider"
        )
        self.canvas.create_oval(
            knob_x - 5, slider_y - 5, knob_x + 5, slider_y + 5,
            fill="#1f201c", outline="", tags="slider"
        )

        # 2. Recuadros de "movimientos" y "Mejor : X movimientos"
        # Caja 1: Movimientos actuales
        self.dibujar_rectangulo_redondeado(
            565, 62, 725, 102, radio=10, 
            fill="#e6e7d4", outline="#4a586e", width=2
        )
        self.canvas.create_text(
            645, 82, text=f"{self.movimientos} movimientos",
            font=("Georgia", 14, "italic"), fill="#333333"
        )

        # Caja 2: Mejor puntuación teórica (2^n - 1)
        mejor = (2 ** self.num_discos) - 1
        self.dibujar_rectangulo_redondeado(
            565, 96, 825, 136, radio=10, 
            fill="#e6e7d4", outline="#4a586e", width=2
        )
        self.canvas.create_text(
            695, 116, text=f"Mejor : {mejor} movimientos",
            font=("Georgia", 14, "italic"), fill="#333333"
        )

        # 3. Botón de Reinicio (esquina superior derecha)
        self.canvas.create_text(
            845, 75, text="↻", font=("Arial", 24, "bold"), 
            fill="#6e7065", tags="btn_reiniciar"
        )

        # Botón extra para Auto-Resolver (Demostración algorítmica)
        color_btn = "#d9534f" if self.auto_resolviendo else "#4a6491"
        texto_btn = "Detener Auto" if self.auto_resolviendo else "▶ Auto-Resolver"
        self.dibujar_rectangulo_redondeado(
            40, 62, 185, 100, radio=8, fill=color_btn, outline="#2b3d5b", width=2, tags="btn_auto"
        )
        self.canvas.create_text(
            112, 81, text=texto_btn, font=("Arial", 11, "bold"), fill="white", tags="btn_auto"
        )

        # 4. Zonas rectangulares sombreadas detrás de cada torre
        for i, px in enumerate(self.postes_x):
            borde = "#3b5998" if self.torre_seleccionada == i else ""
            grosor = 2 if self.torre_seleccionada == i else 0
            self.canvas.create_rectangle(
                px - 95, self.poste_top_y + 15, px + 95, self.base_y,
                fill="#dde0bd", outline=borde, width=grosor
            )

        # 5. Postes verticales y Base horizontal de madera marrón
        for px in self.postes_x:
            self.canvas.create_rectangle(
                px - 5, self.poste_top_y, px + 5, self.base_y,
                fill="#5c3a21", outline="#472b16"
            )
        # Base horizontal
        self.canvas.create_rectangle(
            145, self.base_y, 775, self.base_y + 14,
            fill="#5c3a21", outline="#472b16"
        )

        # 6. Dibujar los discos en cada torre
        altura_total_disponible = 245
        alto_disco = min(22, max(14, altura_total_disponible // max(1, self.num_discos)))
        ancho_min = 28
        ancho_max = 180

        for idx_torre, torre in enumerate(self.torres):
            px = self.postes_x[idx_torre]
            for nivel, tamano_disco in enumerate(torre):
                # Si el disco se está arrastrando con el ratón, lo dibujamos al final
                if (self.disco_arrastrado is not None and 
                    self.torre_origen_arrastre == idx_torre and 
                    nivel == len(torre) - 1):
                    continue

                if self.num_discos == 1:
                    ancho = 100
                else:
                    ancho = ancho_min + (tamano_disco - 1) * (ancho_max - ancho_min) / (self.num_discos - 1)

                y2 = self.base_y - nivel * alto_disco
                y1 = y2 - alto_disco + 1

                # Alternar colores azul oscuro y azul claro como en la imagen
                relleno = "#1e48c7" if tamano_disco % 2 == 1 else "#6c87d6"
                borde_disco = "#102a7a"

                self.dibujar_rectangulo_redondeado(
                    px - ancho / 2, y1, px + ancho / 2, y2,
                    radio=5, fill=relleno, outline=borde_disco, width=2
                )

        # 7. Si hay un disco arrastrándose en el aire, dibujarlo bajo el cursor
        if self.disco_arrastrado is not None:
            tamano_disco, cx, cy = self.disco_arrastrado
            ancho = 100 if self.num_discos == 1 else (
                ancho_min + (tamano_disco - 1) * (ancho_max - ancho_min) / (self.num_discos - 1)
            )
            relleno = "#1e48c7" if tamano_disco % 2 == 1 else "#6c87d6"
            self.dibujar_rectangulo_redondeado(
                cx - ancho / 2, cy - alto_disco / 2, cx + ancho / 2, cy + alto_disco / 2,
                radio=5, fill=relleno, outline="#102a7a", width=2
            )

    # =================== LÓGICA DE INTERACCIÓN ===================

    def obtener_torre_cercana(self, x):
        """Determina a qué poste (0, 1 o 2) corresponde la coordenada X."""
        distancias = [abs(x - px) for px in self.postes_x]
        if min(distancias) < 110:
            return distancias.index(min(distancias))
        return None

    def al_presionar_raton(self, event):
        x, y = event.x, event.y

        # Clic en botón Reiniciar (↻)
        if 825 <= x <= 870 and 55 <= y <= 100:
            self.reiniciar_juego()
            return

        # Clic en botón Auto-Resolver
        if 40 <= x <= 185 and 62 <= y <= 100:
            self.alternar_auto_resolucion()
            return

        if self.auto_resolviendo:
            return

        # Clic o arrastre sobre el Slider de discos
        if 355 <= x <= 545 and 65 <= y <= 105:
            self.actualizar_slider(x)
            self.arrastrando_slider = True
            return
        self.arrastrando_slider = False

        # Interacción con las torres
        idx_torre = self.obtener_torre_cercana(x)
        if idx_torre is not None and 200 <= y <= 520:
            # Si ya había una torre seleccionada por clic, intentar mover ahí
            if self.torre_seleccionada is not None:
                self.intentar_mover(self.torre_seleccionada, idx_torre)
                self.torre_seleccionada = None
                self.dibujar_escena()
                return

            # Si la torre tiene discos, iniciar arrastre / selección
            if self.torres[idx_torre]:
                self.torre_origen_arrastre = idx_torre
                disco_superior = self.torres[idx_torre][-1]
                self.disco_arrastrado = (disco_superior, x, y)
                self.torre_seleccionada = idx_torre
                self.dibujar_escena()

    def al_arrastrar_raton(self, event):
        if getattr(self, "arrastrando_slider", False):
            self.actualizar_slider(event.x)
            return

        if self.disco_arrastrado is not None:
            tamano_disco, _, _ = self.disco_arrastrado
            self.disco_arrastrado = (tamano_disco, event.x, event.y)
            self.dibujar_escena()

    def al_soltar_raton(self, event):
        if getattr(self, "arrastrando_slider", False):
            self.arrastrando_slider = False
            return

        if self.disco_arrastrado is not None:
            destino = self.obtener_torre_cercana(event.x)
            origen = self.torre_origen_arrastre
            self.disco_arrastrado = None
            self.torre_origen_arrastre = None

            if destino is not None and destino != origen:
                self.intentar_mover(origen, destino)
                self.torre_seleccionada = None
            self.dibujar_escena()

    def actualizar_slider(self, x):
        """Actualiza el número de discos entre 1 y 13 según la posición del ratón."""
        slider_x1, slider_x2 = 370, 530
        x_lim = max(slider_x1, min(slider_x2, x))
        nuevo_n = round(1 + ((x_lim - slider_x1) / (slider_x2 - slider_x1)) * 12)
        if nuevo_n != self.num_discos:
            self.num_discos = nuevo_n
            self.reiniciar_juego()

    def intentar_mover(self, origen, destino):
        """Valida las reglas de la Torre de Hanói y ejecuta el movimiento."""
        if not self.torres[origen] or origen == destino:
            return False

        disco = self.torres[origen][-1]
        # Regla: No se puede colocar un disco más grande sobre uno más pequeño
        if not self.torres[destino] or self.torres[destino][-1] > disco:
            self.torres[origen].pop()
            self.torres[destino].append(disco)
            self.movimientos += 1
            self.dibujar_escena()
            self.verificar_victoria()
            return True
        return False

    def verificar_victoria(self):
        """Comprueba si todos los discos llegaron a la tercera torre."""
        if len(self.torres[2]) == self.num_discos and not self.auto_resolviendo:
            mejor = (2 ** self.num_discos) - 1
            messagebox.showinfo(
                "¡Completado!",
                f"¡Has resuelto la Torre de Hanói de {self.num_discos} discos!\n\n"
                f"Tus movimientos: {self.movimientos}\n"
                f"Mejor posible: {mejor} movimientos"
            )

    # =================== AUTO-RESOLUCIÓN ANIMADA ===================

    def alternar_auto_resolucion(self):
        if self.auto_resolviendo:
            self.reiniciar_juego()
            return

        self.reiniciar_juego()
        self.auto_resolviendo = True
        self.cola_movimientos = []
        self.generar_movimientos_recursivos(self.num_discos, 0, 2, 1)
        self.animar_siguiente_paso()

    def generar_movimientos_recursivos(self, n, origen, destino, auxiliar):
        if n == 1:
            self.cola_movimientos.append((origen, destino))
            return
        self.generar_movimientos_recursivos(n - 1, origen, auxiliar, destino)
        self.cola_movimientos.append((origen, destino))
        self.generar_movimientos_recursivos(n - 1, auxiliar, destino, origen)

    def animar_siguiente_paso(self):
        if not self.auto_resolviendo or not self.cola_movimientos:
            self.auto_resolviendo = False
            self.dibujar_escena()
            return

        origen, destino = self.cola_movimientos.pop(0)
        self.intentar_mover(origen, destino)
        # Velocidad adaptativa: más rápido si hay muchos discos
        delay = max(15, int(400 / (self.num_discos ** 1.3)))
        self.after_id = self.root.after(delay, self.animar_siguiente_paso)

if __name__ == "__main__":
    ventana = tk.Tk()
    app = TorreDeHanoiInteractivo(ventana)
    ventana.mainloop()
