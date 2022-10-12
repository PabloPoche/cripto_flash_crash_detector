'''
trend.py 
Contiene las funciones encargadas de adquirir, graficar y evaluar el precio de una criptomoneda

- get_cripto:   Adquiere de Binance en precio de una determinada criptomoneda
- get_x_y_sp:   Enlista precio/tiempo, calcula el nivel de fc(set point) y evalua si se produjo el evento
- trending:     Grafica a tiempo real el precio de una determinada criptomoneda

'''

import requests
import datetime as dt

import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import keyboard
import graph
import send_sms


def get_cripto(cripto):
    url = "https://api.binance.com/api/v3/ticker/price?symbol="+ cripto +"USDT"
    data= requests.get(url).json()      # Extraer el JSON de la (url)
    if data.get("code") == -1121 :      # Moneda ingresada valida ?
        return(False)
    price =float(data.get("price"))
    time= dt.datetime.now() 
    return (time, price)
    

def get_x_y_sp(cripto):
    time, price= get_cripto(cripto)
    
    global x, y, sp
    global tiempo, precio, s_p
    global fc                           # necesario para escribir las variables globales 

    x.append(time)
    y.append(price)
    set_point= max(y)-(max(y)/100)      # caida del 1% de la cripto
    sp.append(set_point)    
    
    if fc is True:
        tiempo.append(time)             # continuar registro posterior al evento
        precio.append(price)
        s_p.append(set_point) 
    else:
        if keyboard.is_pressed("t"):    # Forced flash crash  ?
            y[-1]= sp[-1]
        if y[-1] <= sp[-1]:             # Normal flash crash  ?
            tiempo=list(x) 
            precio=list(y)              # registro 1 min previo al evento
            s_p= list(sp)     
            #send_sms.send(cripto)       # enviar SMS al usuario(solo usuarios registrados, VER send_sms.py)
            fc= True                    # Set flag (flash crash detectado)
         
    if len(x) > 55:                     # control de rotacion en x (ventana 1 min. aprox)
        x.pop(0)
        y.pop(0)
        sp.pop(0)
    
    return (x, y, sp)


def reload(frame):
    
    if len(tiempo) == 100:               # registro 1 min posterior al evento ?
        plt.close(plt.gcf())             # finalizar trending
    else:
        x, y, sp= get_x_y_sp(cripto)

        plt.get_current_fig_manager().set_window_title("Trending...")   # titulo de la ventana

        if fc == True :
            if frame % 2 == 0:
                text= "*** Flash Crash detectado ***"
            else:
                text= "...enviando SMS al usuario..."
        else: 
            text= "Presione:  (t) para forzar flash crash  o  (q) para salir."
        
        graph.graf_frame(x, y, sp, cripto, text)                # Define marco de la ventana grafica
        
          

def trending(crypto):

    global cripto
    cripto= crypto

    global x
    global y
    global sp

    global tiempo
    global precio
    global s_p

    x = [] 
    y = [] 
    sp= [] 
    
    tiempo = [] 
    precio = [] 
    s_p= [] 

    global fc
    fc= False                           # Clear flag (flash crash no detectado)

    plt.rcParams['toolbar'] = "None"    # quitar barra de herramientas de matplotlib 
    plt.style.use("seaborn")            # Estilo del grafico
    #plt.figure(figsize=(12,6))          # Tamaño del grafico
    plt.get_current_fig_manager().full_screen_toggle()  # Full screen
    
    # Graficar trending...
    animation = FuncAnimation(plt.gcf(), reload, interval=500)
    plt.show()
    print("Trending finalizado")
    return (precio, tiempo, s_p)


