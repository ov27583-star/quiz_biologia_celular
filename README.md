# Quiz de Biología Celular

Aplicación interactiva con interfaz gráfica desarrollada en **Python** y **Tkinter** para repasar y evaluar conocimientos de biología celular a partir de preguntas cargadas desde un archivo JSON.

## Características y funcionamiento

- **Interfaz gráfica de tres pantallas (`QuizApp`):**
  - **Inicio:** Solicita el nombre del jugador antes de comenzar (valida que el campo no esté vacío).
  - **Juego:** Muestra el número de pregunta actual, el puntaje acumulado, el enunciado y opciones en formato de casillas (`Checkbutton`) distribuidas en dos columnas, permitiendo preguntas de una o varias respuestas correctas[cite: 12].
  - **Resultados:** Despliega el nombre del jugador, el puntaje final, el conteo de aciertos y fallos, además de una ventana emergente con el resumen y un botón para volver al inicio.
- **Sistema de puntuación:**
  - **Acierto exacto:** `+15` puntos (la selección debe coincidir exactamente con los índices indicados en `"correctas"`).
  - **Respuesta incorrecta:** `-5` puntos.
- **Validación del banco de preguntas (`cargar_preguntas`):**
  - Lee `preguntas.json` en codificación `UTF-8`.
  - Verifica que el contenido sea una lista con **al menos 5 preguntas**.
  - Muestra alertas gráficas (`messagebox`) si el archivo no existe, tiene errores de formato JSON o no cumple con el mínimo de preguntas.
  
### Cómo ejecutar el programa
1. Asegúrate de tener `quiz_biologia_celular.py` y `preguntas.json` en la misma carpeta[cite: 5, 10, 12].
2. Abre una terminal dentro de la carpeta del proyecto y ejecuta

#### Estructura del proyecto

```text
quiz_biologia_celular/
├── quiz_biologia_celular.py   # Interfaz gráfica (Tkinter), validación y lógica del quiz
├── preguntas.json             # Banco de preguntas, opciones e índices correctos
├── .gitignore                 # Excluye .venv/ y archivos no deseados de Git
└── README.md                  # Documentación del proyecto