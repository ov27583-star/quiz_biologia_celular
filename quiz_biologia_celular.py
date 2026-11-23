import json
import tkinter as tk
from tkinter import messagebox


def cargar_preguntas():
    try:
        with open("preguntas.json", "r", encoding="utf-8") as f:
            preguntas = json.load(f)
        if not isinstance(preguntas, list) or len(preguntas) < 5:
            messagebox.showerror(
                "Error", "Se necesitan al menos 5 preguntas en el archivo JSON"
            )
            return None
        return preguntas
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo preguntas.json")
        return None
    except json.JSONDecodeError:
        messagebox.showerror("Error", "El archivo JSON tiene un error de formato")
        return None


class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz de Biología Celular")
        self.root.geometry("580x420")

        # Cargar preguntas
        self.preguntas = cargar_preguntas()
        if not self.preguntas:
            self.root.destroy()
            return

        # Variables del juego
        self.nombre_jugador = ""
        self.indice_actual = 0
        self.puntaje = 0
        self.aciertos = 0
        self.fallos = 0
        self.opcion_vars = []

        # Crear pantallas
        self.crear_frame_inicio()
        self.crear_frame_juego()
        self.crear_frame_resultados()

        # Mostrar pantalla inicial
        self.mostrar_frame(self.frame_inicio)

    def mostrar_frame(self, frame_visible):
        self.frame_inicio.pack_forget()
        self.frame_juego.pack_forget()
        self.frame_resultados.pack_forget()
        frame_visible.pack(fill="both", expand=True)

    def crear_frame_inicio(self):
        self.frame_inicio = tk.Frame(self.root, padx=20, pady=60, bg="#e8f4f8")
        self.frame_inicio.pack_propagate(False)

        tk.Label(
            self.frame_inicio,
            text="🧬 Quiz de Biología Celular",
            font=("Times New Roman", 22, "bold"),
            bg="#e8f4f8",
            fg="#2c3e50",
        ).pack(pady=20)

        tk.Label(
            self.frame_inicio,
            text="Ingrese su nombre:",
            font=("Times New Roman", 14),
            bg="#e8f4f8",
            fg="#2c3e50",
        ).pack(pady=10)

        self.entry_nombre = tk.Entry(
            self.frame_inicio,
            font=("Times New Roman", 14),
            width=25,
            justify="center",
        )
        self.entry_nombre.pack(pady=15)

        tk.Button(
            self.frame_inicio,
            text="Iniciar Juego",
            font=("Times New Roman", 14, "bold"),
            command=self.al_pulsar_iniciar,
            bg="#27ae60",
            fg="white",
            padx=20,
            pady=6,
        ).pack(pady=10)

    def crear_frame_juego(self):
        self.frame_juego = tk.Frame(self.root, padx=20, pady=20, bg="#fef9e7")
        self.frame_juego.pack_propagate(False)

        self.lbl_numero_pregunta = tk.Label(
            self.frame_juego,
            text="",
            font=("Times New Roman", 10, "bold"),
            bg="#fef9e7",
            fg="#8d6e00",
        )
        self.lbl_numero_pregunta.pack(anchor="w", pady=5)

        self.lbl_puntaje = tk.Label(
            self.frame_juego,
            text="",
            font=("Times New Roman", 10),
            bg="#fef9e7",
            fg="#8d6e00",
        )
        self.lbl_puntaje.pack(anchor="w", pady=5)

        self.lbl_pregunta = tk.Label(
            self.frame_juego,
            text="",
            font=("Times New Roman", 14, "bold"),
            wraplength=540,
            justify="left",
            bg="#fef9e7",
            fg="#2c3e50",
        )
        self.lbl_pregunta.pack(pady=15)

        self.frame_opciones = tk.Frame(self.frame_juego, bg="#fef9e7")
        self.frame_opciones.pack(pady=10)

        self.btn_validar = tk.Button(
            self.frame_juego,
            text="Validar Respuesta",
            command=self.al_pulsar_validar,
            font=("Times New Roman", 11, "bold"),
            bg="#3498db",
            fg="white",
            padx=30,
            pady=6,
        )
        self.btn_validar.pack(pady=20)

    def crear_frame_resultados(self):
        self.frame_resultados = tk.Frame(self.root, padx=20, pady=50, bg="#eafaf1")
        self.frame_resultados.pack_propagate(False)

        tk.Label(
            self.frame_resultados,
            text="🏆 ¡Fin del Quiz!",
            font=("Times New Roman", 20, "bold"),
            bg="#eafaf1",
            fg="#1e8449",
        ).pack(pady=10)

        self.lbl_nombre_final = tk.Label(
            self.frame_resultados,
            text="",
            font=("Times New Roman", 12),
            bg="#eafaf1",
            fg="#2c3e50",
        )
        self.lbl_nombre_final.pack(pady=5)

        self.lbl_puntaje_final = tk.Label(
            self.frame_resultados,
            text="",
            font=("Times New Roman", 16, "bold"),
            bg="#eafaf1",
            fg="#1e8449",
        )
        self.lbl_puntaje_final.pack(pady=10)

        self.lbl_estadisticas = tk.Label(
            self.frame_resultados,
            text="",
            font=("Times New Roman", 12),
            bg="#eafaf1",
            fg="#2c3e50",
        )
        self.lbl_estadisticas.pack(pady=10)

        tk.Button(
            self.frame_resultados,
            text="Volver al Inicio",
            command=self.volver_al_inicio,
            font=("Times New Roman", 12, "bold"),
            bg="#f39c12",
            fg="white",
            padx=30,
            pady=8,
        ).pack(pady=20)

    def al_pulsar_iniciar(self):
        nombre = self.entry_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Aviso", "Por favor escribe tu nombre")
            return

        self.nombre_jugador = nombre
        self.indice_actual = 0
        self.puntaje = 0
        self.aciertos = 0
        self.fallos = 0

        self.mostrar_frame(self.frame_juego)
        self.actualizar_pantalla_pregunta()

    def actualizar_pantalla_pregunta(self):
        for var in self.opcion_vars:
            var.set(0)
        self.opcion_vars.clear()

        for widget in self.frame_opciones.winfo_children():
            widget.destroy()

        pregunta = self.preguntas[self.indice_actual]

        self.lbl_numero_pregunta.config(
            text=f"Pregunta {self.indice_actual + 1} de {len(self.preguntas)}"
        )
        self.lbl_puntaje.config(text=f"Puntaje actual: {self.puntaje} puntos")
        self.lbl_pregunta.config(text=pregunta["pregunta"])

        for i, texto_opcion in enumerate(pregunta["opciones"]):
            fila = i // 2
            columna = i % 2

            var = tk.IntVar(value=0)
            self.opcion_vars.append(var)

            chk = tk.Checkbutton(
                self.frame_opciones,
                text=texto_opcion,
                variable=var,
                font=("Times New Roman", 11),
                bg="#fef9e7",
                fg="#2c3e50",
            )
            chk.grid(row=fila, column=columna, sticky="w", padx=20, pady=5)

    def al_pulsar_validar(self):
        pregunta_actual = self.preguntas[self.indice_actual]
        indices_correctos = set(pregunta_actual["correctas"])

        indices_seleccionados = {
            i for i, var in enumerate(self.opcion_vars) if var.get() == 1
        }

        if indices_seleccionados == indices_correctos:
            self.puntaje += 15
            self.aciertos += 1
            mensaje = "¡Correcto! +15 puntos"
        else:
            self.puntaje -= 5
            self.fallos += 1
            mensaje = " Incorrecto. -5 puntos"

        messagebox.showinfo("Resultado", mensaje)

        self.indice_actual += 1
        if self.indice_actual < len(self.preguntas):
            self.actualizar_pantalla_pregunta()
        else:
            self.mostrar_frame(self.frame_resultados)
            self.mostrar_resultados()

    def mostrar_resultados(self):
        self.lbl_nombre_final.config(text=f"Jugador: {self.nombre_jugador}")
        self.lbl_puntaje_final.config(text=f"Puntaje Final: {self.puntaje} puntos")
        self.lbl_estadisticas.config(
            text=f"✅ Aciertos: {self.aciertos}    |    ❌ Fallos: {self.fallos}"
        )
        messagebox.showinfo(
            "🏆 Resultados Finales",
            f"Jugador: {self.nombre_jugador}\n"
            f"Puntaje total: {self.puntaje}\n"
            f"Aciertos: {self.aciertos}\n"
            f"Fallos: {self.fallos}",
        )

    def volver_al_inicio(self):
        self.entry_nombre.delete(0, tk.END)
        self.mostrar_frame(self.frame_inicio)


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()