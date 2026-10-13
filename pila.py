import tkinter as tk
from tkinter import messagebox


class StackVisualizer:
    """Visualizador gráfico de una pila (LIFO) con Tkinter."""

    BG = "#f3f6fb"
    CARD = "#ffffff"
    INK = "#17253f"
    MUTED = "#687891"
    BLUE = "#3867e8"
    RED = "#d94b5b"
    GREEN = "#168568"

    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Pila | LIFO")
        self.root.geometry("900x680")
        self.root.minsize(720, 580)
        self.root.configure(bg=self.BG)
        self.stack = []
        self._build_ui()
        self._draw_stack()

    def _build_ui(self):
        header = tk.Frame(self.root, bg=self.BG, padx=30, pady=22)
        header.pack(fill="x")
        tk.Label(header, text="ESTRUCTURAS DE DATOS  /  01", bg=self.BG,
                 fg=self.BLUE, font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(header, text="La pila", bg=self.BG, fg=self.INK,
                 font=("Segoe UI", 28, "bold")).pack(anchor="w", pady=(3, 0))
        tk.Label(header, text="Una estructura LIFO: el último elemento en entrar es el primero en salir.",
                 bg=self.BG, fg=self.MUTED, font=("Segoe UI", 11)).pack(anchor="w", pady=(2, 0))

        body = tk.Frame(self.root, bg=self.BG, padx=30, pady=4)
        body.pack(fill="both", expand=True)
        left = tk.Frame(body, bg=self.CARD, padx=20, pady=18,
                        highlightthickness=1, highlightbackground="#e1e7f0")
        left.pack(side="left", fill="both", expand=True)
        right = tk.Frame(body, bg=self.CARD, width=260, padx=18, pady=18,
                         highlightthickness=1, highlightbackground="#e1e7f0")
        right.pack(side="right", fill="y", padx=(16, 0))
        right.pack_propagate(False)

        tk.Label(left, text="Representación de la pila", bg=self.CARD, fg=self.INK,
                 font=("Segoe UI", 13, "bold")).pack(anchor="w")
        tk.Label(left, text="La cima está arriba; cada elemento se retira desde ahí.",
                 bg=self.CARD, fg=self.MUTED, font=("Segoe UI", 9)).pack(anchor="w", pady=(3, 12))
        self.canvas = tk.Canvas(left, bg="#f8faff", highlightthickness=0, height=390)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda _event: self._draw_stack())
        self.status = tk.Label(left, text="La pila está vacía.", bg=self.CARD, fg=self.MUTED,
                               font=("Segoe UI", 10), anchor="w")
        self.status.pack(fill="x", pady=(10, 0))

        tk.Label(right, text="Operaciones", bg=self.CARD, fg=self.INK,
                 font=("Segoe UI", 13, "bold")).pack(anchor="w")
        tk.Label(right, text="Valor para apilar", bg=self.CARD, fg=self.MUTED,
                 font=("Segoe UI", 9)).pack(anchor="w", pady=(16, 5))
        self.entry = tk.Entry(right, font=("Segoe UI", 11), relief="solid", bd=1,
                              highlightthickness=0)
        self.entry.pack(fill="x", ipady=7)
        self.entry.bind("<Return>", lambda _event: self.push())
        self._button(right, "＋  Apilar", self.push, self.BLUE, "#ffffff").pack(fill="x", pady=(10, 7))
        self._button(right, "－  Desapilar", self.pop, "#fff0f1", self.RED).pack(fill="x", pady=4)
        self._button(right, "◎  Ver cima", self.peek, "#eaf7f3", self.GREEN).pack(fill="x", pady=4)
        self._button(right, "↺  Reiniciar", self.clear, "#eef1f6", self.INK).pack(fill="x", pady=(4, 0))

        tk.Frame(right, bg="#e6ebf2", height=1).pack(fill="x", pady=18)
        tk.Label(right, text="¿Cómo funciona?", bg=self.CARD, fg=self.INK,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w")
        tk.Label(right, text="APILAR (push)\nAgrega un elemento en la cima.\n\n"
                            "DESAPILAR (pop)\nRetira el elemento de la cima.\n\n"
                            "VER CIMA (peek)\nConsulta el elemento superior sin retirarlo.",
                 justify="left", bg=self.CARD, fg=self.MUTED,
                 font=("Segoe UI", 9), wraplength=220).pack(anchor="w", pady=(8, 0))
        self.count = tk.Label(right, text="Elementos: 0", bg=self.CARD, fg=self.MUTED,
                              font=("Segoe UI", 9, "bold"))
        self.count.pack(anchor="w", side="bottom", pady=(12, 0))

    @staticmethod
    def _button(parent, text, command, bg, fg):
        return tk.Button(parent, text=text, command=command, bg=bg, fg=fg,
                         activebackground=bg, activeforeground=fg, relief="flat",
                         cursor="hand2", font=("Segoe UI", 10, "bold"), pady=9)

    def push(self):
        value = self.entry.get().strip()
        if not value:
            self.status.config(text="Escribe un valor antes de apilarlo.", fg=self.RED)
            self.entry.focus_set()
            return
        self.stack.append(value)
        self.entry.delete(0, "end")
        self.status.config(text=f"Se apiló «{value}» en la cima.", fg=self.BLUE)
        self._draw_stack()
        self.entry.focus_set()

    def pop(self):
        if not self.stack:
            self.status.config(text="No se puede desapilar: la pila está vacía.", fg=self.RED)
            return
        value = self.stack.pop()
        self.status.config(text=f"Se desapiló «{value}».", fg=self.RED)
        self._draw_stack()

    def peek(self):
        if not self.stack:
            self.status.config(text="La pila está vacía; no hay elemento en la cima.", fg=self.RED)
            return
        self.status.config(text=f"La cima contiene «{self.stack[-1]}». La pila no cambió.", fg=self.GREEN)

    def clear(self):
        self.stack.clear()
        self.status.config(text="Pila reiniciada.", fg=self.MUTED)
        self._draw_stack()

    def _draw_stack(self):
        if not hasattr(self, "canvas"):
            return
        c = self.canvas
        c.delete("all")
        width = max(c.winfo_width(), 300)
        height = max(c.winfo_height(), 250)
        cx = width / 2
        top = 45
        box_w = min(300, width - 90)
        box_h = 48
        gap = 8
        max_visible = max(1, int((height - top - 42) / (box_h + gap)))
        visible = self.stack[-max_visible:]
        if self.stack:
            base_y = height - 36
            c.create_line(cx - box_w / 2 - 20, base_y, cx + box_w / 2 + 20, base_y,
                          fill="#9aabc2", width=3)
            c.create_line(cx - box_w / 2, top - 10, cx - box_w / 2, base_y,
                          fill="#c9d4e3", width=3)
            c.create_line(cx + box_w / 2, top - 10, cx + box_w / 2, base_y,
                          fill="#c9d4e3", width=3)
            for offset, value in enumerate(reversed(visible)):
                y = base_y - box_h - offset * (box_h + gap)
                is_top = (offset == 0)
                fill = "#eaf0ff" if is_top else "#ffffff"
                outline = self.BLUE if is_top else "#cbd5e3"
                c.create_rectangle(cx - box_w / 2, y, cx + box_w / 2, y + box_h,
                                   fill=fill, outline=outline, width=2 if is_top else 1)
                label = str(value)
                if len(label) > 28:
                    label = label[:25] + "..."
                c.create_text(cx, y + box_h / 2, text=label, fill=self.INK,
                              font=("Segoe UI", 11, "bold" if is_top else "normal"))
                if is_top:
                    c.create_text(cx + box_w / 2 + 36, y + box_h / 2, text="CIMA",
                                  fill=self.BLUE, font=("Segoe UI", 8, "bold"))
            hidden = len(self.stack) - len(visible)
            if hidden:
                c.create_text(cx, height - 12, text=f"↑  {hidden} elemento(s) más abajo",
                              fill=self.MUTED, font=("Segoe UI", 9))
        else:
            c.create_text(cx, height / 2 - 6, text="La pila está vacía",
                          fill=self.MUTED, font=("Segoe UI", 13))
            c.create_text(cx, height / 2 + 22, text="Usa «Apilar» para agregar el primer elemento",
                          fill="#97a5ba", font=("Segoe UI", 9))
        self.count.config(text=f"Elementos: {len(self.stack)}")


def main():
    root = tk.Tk()
    StackVisualizer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
 