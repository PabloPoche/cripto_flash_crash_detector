'''
graph.py 
Contiene las funciones encargadas de graficar(Matplotlib) el registro completo(DB) y presentarlo en HTML

- graf_frame:   Define el marco de grafico
- plot_xy:      Grafica el registro completo de la BD y lo enviar al front-end en formato HTML.

'''

import io
import base64
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

# Para convertir matplotlib a imagen y luego a datos binarios
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigureCanvas


def graf_frame(cripto, tiempo, precio, s_p, text):
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
    plt.plot(tiempo, precio)
    # dibujar linea horizontal
    plt.axhline(max(s_p), color= "red", linewidth= 1, linestyle= "dashed")
    plt.text(tiempo[0] ,max(s_p), "Set point(-1%)", color = "red", fontsize=10, va='center', ha='center', backgroundcolor='w')
    plt.tight_layout()
    return


def plot_xy(cripto, tiempo, precio, s_p):
    plt.style.use("seaborn")            # Estilo del grafico
    fig= plt.figure(figsize=(16,9))     # Tamaño del grafico
    text= "Presione:  (Ctrl p) para imprimir grafico  o  (Alt ←) para volver al menu principal."
    graf_frame(cripto, tiempo, precio, s_p, text) # Define marco de la ventana grafica
    image_html = io.BytesIO()           # Convertir ese grafico en una imagen para enviar por HTTP y mostrar en el HTML
    FigureCanvas(fig).print_png(image_html)
    plt.close(fig)                      # Cerrar la imagen para que no consuma memoria del sistema
    return image_html

