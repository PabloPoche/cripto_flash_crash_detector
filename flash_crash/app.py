'''
Curso de Python
Proyecto integrador del nivel programador

Autor: Pablo Pochettino
Version: 1.0 (09/10/2022)

------------------------------------------- Cripto Flash Crash Detector --------------------------------
Un Flash Crash es un evento muy poco frecuente que se da en los mercados financieros en el que un activo, 
en este caso una criptomoneda, cae rápidamente de valor (caída de más del 1% en menos de 1 minuto).
La aplicación monitorea el precio de una determinada criptomoneda y en caso de detectarse un flash crash de la misma notifica
al usuario vía SMS, registra el evento completo(minuto previo y posterior al evento) en una BD y posibilita luego exportarlo 
a una archivo .csv para un posterior análisis(Data Analytic)


Revision 1.1 (20/10/2022)
Se realiza la grafica a tiempo real(trending) mediante Java script(Chart.js) con una comunicacion de datos SSE(Server-sent events)
 hacia el cliente(front end).


Para ejecutar la aplicacion ingrese a la URL: 
http://127.0.0.1:5000/

'''
import time
from datetime import datetime

import time, os
import traceback
import json
from types import ClassMethodDescriptorType
from flask import Flask, request, jsonify, render_template, Response, redirect

import trend
import graph
import sql_db
import export_csv


# Crear el server Flask
app = Flask(__name__)

# Indicamos al sistema (app) de donde leer la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flash_crash.db"
# Asociamos nuestro controlador de la base de datos con la aplicacion
sql_db.db.init_app(app)
app.app_context().push()
sql_db.db.create_all()
sms= " "


# Ruta que se ingresa por la ULR 127.0.0.1:5000
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        try:
            print("Menu principal")
            return render_template("index.html")
        except:
            return jsonify({'trace': traceback.format_exc()})

    if request.method == "POST":
        try:
            # Obtener del HTTP POST JSON el nombre de la cripto
            global cripto
            cripto = str(request.form.get("name")).upper()
            print(cripto)
           
            if trend.test_cripto(cripto) == False:
                no_cripto= "  (moneda inexistente, reingrese)"
                print(no_cripto)
                return render_template("index.html", namei= no_cripto)

            print("Iniciar trenging")

            # Carga pagina con script(java) encargado de graficar a tiempo real en el front-end
            return render_template("trend.html", namet= cripto)
        except:
            return jsonify({'trace': traceback.format_exc()})


# Ruta que se ingresa por la ULR 127.0.0.1:5000/graficar
@app.route("/graficar")
def graficar():
        try:
            print("Graficar/Imprimir ultimo flash crash.")
            # Recuperar de la DB los datos del ultimo flash crash
            
            # Pasar los datos a listas
            cripto, tiempo, precio, s_p= sql_db.db_to_lists()

            # Transformar los datos de las listas en una imagen HTML con matplotlib
            image_html = graph.plot_xy(cripto[0], tiempo, precio, s_p)
            return Response(image_html.getvalue(), mimetype='image/png')
        except:
            return jsonify({'trace': traceback.format_exc()})


# Ruta que se ingresa por la ULR 127.0.0.1:5000/exportar
@app.route("/exportar")
def exportar():
        try:
            print("Exportar a archivo .cvs")

            # pasar los datos de la BD a listas
            cripto, tiempo, precio, s_p= sql_db.db_to_lists()

            # exportar listas a un archivo(flash_crash.csv)
            export_csv.lists_to_csv(cripto, tiempo, precio, s_p)

            # hora y fecha de la ultima actualizacion
            mod = os.path.getmtime("flash_crash.csv")
            year,month,day,hour,minute,second=time.localtime(mod)[:-3]
            act= "%02d:%02d:%02d  (%02d/%02d/%d)"%(hour,minute,second,day,month,year)
            exp_date= "flash_crash.csv actualizado: " + act
            print(exp_date)

            return render_template("index.html", name= exp_date)
        except:
            return jsonify({'trace': traceback.format_exc()})


# Envio de datos hacia el front end mediante SSE(Server-sent events)
@app.route("/sse")
def sse():
    def loop():
        while True:
            global sms
            cripto, tim, price, set_point, sms= trend.get_all()
           
            if sms == "backup":
               break

            tim= tim.strftime("%H:%M:%S")
            # Armo json para enviar al front-end cada 1 seg. aprox  
            json_data = json.dumps({"cripto": cripto, "time": tim, "price": price, "sp": set_point, "sms": sms})
            yield f"data:{json_data}\n\n"
            time.sleep(0.5)
            print(json_data)

    if sms == "backup":     
        print("Base de datos creada")
        # Borrar y crear una nueva tabla flash_crash_sql en la BD
        sql_db.db.drop_all()
        sql_db.db.create_all()
        # cargar datos del nuevo flash_crash en la BD
        cripto, tiempo, precio, s_p= trend.get_list()
        sql_db.lists_to_db(cripto, tiempo, precio, s_p)
        print("Base de datos actualizada")

    return Response(loop(), mimetype='text/event-stream')
       


if __name__ == '__main__':
    print("Server start!")

    # Lanzar server
    app.run(host="127.0.0.1", port=5000, threaded=True)
    
            