'''
graph.py 
Contiene las funciones encargadas de graficar el registro completo(DB) en HTML

- graf_frame:   Define el marco de grafico
- plot_xy:      Grafica el registro completo de la BD y lo enviar al front-end en HTML.

'''

import io
import base64
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

# Para convertir matplotlib a imagen y luego a datos binarios
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigureCanvas


def graf_frame(x, y, sp, cripto, text):
    plt.cla()
    plt.title(text, color = "red") 
    # titulo del grafico y etiquetas de los ejes
    plt.suptitle( cripto + " Flash Crash Detector", fontsize=15) 
    plt.xlabel("Tiempo") 
    plt.ylabel("Precio "+ cripto + "/USDT")
    # quitar notacion cientifica
    plt.ticklabel_format(useOffset=False, style="plain")
    # rotacion de fechas eje x
    plt.xticks(rotation=90)
    plt.plot(x, y)
    # dibujar linea horizontal
    plt.axhline(max(sp), color= "red", linewidth= 1, linestyle= "dashed")
    plt.text(x[0] ,max(sp), "Set point(-1%)", color = "red", fontsize=10, va='center', ha='center', backgroundcolor='w')
    plt.tight_layout()
    return


def plot_xy(cripto, y, x, sp):
    plt.style.use("seaborn")            # Estilo del grafico
    fig= plt.figure(figsize=(16,9))     # Tamaño del grafico
    text= "Presione:  (Ctrl p) para imprimir grafico  o  (Alt ←) para volver al menu principal."
    graf_frame(x, y, sp, cripto, text) # Define marco de la ventana grafica
    image_html = io.BytesIO()           # Convertir ese grafico en una imagen para enviar por HTTP y mostrar en el HTML
    FigureCanvas(fig).print_png(image_html)
    plt.close(fig)                      # Cerrar la imagen para que no consuma memoria del sistema
    return image_html



