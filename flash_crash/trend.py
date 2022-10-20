'''
trend.py 
Contiene las funciones encargadas de adquirir, almacenar y evaluar el precio de una criptomoneda

- test_cripto:  Veifica exista la criptomoneda ingresada
- get_cripto:   Adquiere de Binance en precio de una determinada criptomoneda
- get_all:      Enlista todas las variables, calcula el nivel de fc(set point) y evalua si se produjo el evento
- get_list:     Retorna las lista de las variables registradas durante todo el evento.

'''

import requests
import datetime as dt
import keyboard
import send_sms


def test_cripto(cripto):

    global crypto
    crypto= " "
    crypto= cripto
  
    global tiempo
    global precio
    global s_p
    global sms
    
    tiempo = [] 
    precio = [] 
    s_p= [] 
    sms= " "

    global fc
    fc= False                           # Clear flag (flash crash no detectado)
   
    if get_cripto(cripto) == False:
        return(False)
    return(True)


def get_cripto(cripto):
    url = "https://api.binance.com/api/v3/ticker/price?symbol="+ cripto +"USDT"
    data= requests.get(url).json()      # Extraer el JSON de la (url)
    if data.get("code") == -1121 :      # Moneda ingresada valida ?
        return(False)
    price =float(data.get("price"))
    time= dt.datetime.now()
    return (time, price)
    

def get_all():
   
    global tiempo, precio, s_p          # necesario para escribir las variables globales 
    global fc
    global cripto
    cripto= crypto

    time, price= get_cripto(cripto)     # toma de valores instantaneos
    
    global tiempo, precio, s_p          # necesario para escribir las variables globales
    tiempo.append(time)
    precio.append(price)
    set_point= max(precio)-(max(precio)/100)      # calculo del flash crash level (1%)
    s_p.append(set_point)    
    
    if keyboard.is_pressed("t") and fc is False:   # Forced flash crash  ?
        price=  s_p[-1] 
        precio[-1]= s_p[-1]
    
    if  precio[-1] <= s_p[-1]:                      # Normal flash crash  ?
          # send_sms.send(cripto)       # enviar SMS al usuario(solo usuarios registrados, VER send_sms.py)
        fc= True                                    # Set flag (flash crash detectado)
    global sms
    if fc == True :
        if len(tiempo) % 2 == 0:
            sms= "*** Flash Crash detectado ***"
        else:
            sms= "...enviando SMS al usuario..."
    else: 
        sms= "Presione:  (t) para forzar flash crash  o  (Alt ←) para volver al menu principal."
    
    if len(tiempo) > 60 and fc is False:       # mientras no haya flash crash solo se almacena el ultimo minuto.
        tiempo.pop(0)
        precio.pop(0)
        s_p.pop(0)
    
    print(len(tiempo))
    
    if len(tiempo) == 120:      # actualizar BD luego de 1min de ocurrido el flash crash
        print("Backup en DB del trending completo")
        sms= "backup"
    
    if len(tiempo) > 120:       # cierra ventana de trending luego actualizar la BD.
        print("Trending finalizado, carrar ventana de trending")
        sms= "fin"
    return (cripto, time, price, set_point, sms) # retorno de valores instantaneos

def get_list():
    return (cripto, tiempo, precio, s_p)          # retorno de listas de valores instantaneos

