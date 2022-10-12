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

Para ejecutar la aplicacion ingrese a la URL: 
http://127.0.0.1:5000/

'''

import time, os
import traceback
from flask import Flask, request, jsonify, render_template, Response, redirect, url_for

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
            
            cripto = str(request.form.get("name")).upper()
            print(cripto)
            
            if trend.get_cripto(cripto) == False:
                no_cripto= "  (moneda inexistente, reingrese)"
                print(no_cripto)
                return render_template("index.html", namei= no_cripto)

            print("Iniciar trenging")
            # iniciar trending hasta que se de un flash_crash o presione (q)
            precio, tiempo, s_p= trend.trending(cripto)

            if len(tiempo) == 100:      # actualizar BD solo si se produjo un flash crash
                # Borrar y crear una nueva tabla flash_crash_sql en la BD
                sql_db.db.drop_all()
                sql_db.db.create_all()
                print("Base de datos creada")

                # cargar datos del nuevo flash_crash en la BD
                sql_db.lists_to_db(cripto, precio, tiempo, s_p)
                print("Base de datos actualizada")

            # Como respuesta al POST devolvemos la tabla de valores
            return render_template("index.html")
        except:
            return jsonify({'trace': traceback.format_exc()})


# Ruta que se ingresa por la ULR 127.0.0.1:5000/graficar
@app.route("/graficar")
def graficar():
        try:
            print("Graficar/Imprimir ultimo flash crash.")
            # Recuperar de la DB los datos del ultimo flash crash
            
            # Pasar los datos a listas
            cripto, precio, tiempo, s_p= sql_db.db_to_lists()

            # Transformar los datos de las listas en una imagen HTML con matplotlib
            image_html = graph.plot_xy(cripto[0], precio, tiempo, s_p)
            return Response(image_html.getvalue(), mimetype='image/png')
        except:
            return jsonify({'trace': traceback.format_exc()})


# Ruta que se ingresa por la ULR 127.0.0.1:5000/exportar
@app.route("/exportar")
def exportar():
        try:
            print("Exportar a archivo .cvs")

            # pasar los datos de la BD a listas
            cripto, precio, tiempo, s_p= sql_db.db_to_lists()

            # exportar listas a un archivo(flash_crash.csv)
            export_csv.lists_to_csv(cripto, precio, tiempo, s_p)

            # hora y fecha de la ultima actualizacion
            mod = os.path.getmtime("flash_crash.csv")
            year,month,day,hour,minute,second=time.localtime(mod)[:-3]
            act= "%02d:%02d:%02d  (%02d/%02d/%d)"%(hour,minute,second,day,month,year)
            exp_date= "flash_crash.csv actualizado: " + act
            print(exp_date)

            return render_template("index.html", name= exp_date)
        except:
            return jsonify({'trace': traceback.format_exc()})



if __name__ == '__main__':
    print("Server start!")

    # Lanzar server
    app.run(host="127.0.0.1", port=5000)