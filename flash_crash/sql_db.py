'''
sql_db.py 
Contiene las funciones encargadas de crear y administrar la DB(flash_crash.db)

- Crear una nueva BD (sobre escribe la anterior)
- insert:         Insertar una nueva fila en la BD
- lists_to_db:    Cargar las listas en la BD
- db_to_lists:    Cargar las listas con la DB

'''
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()



    # Crea una nueva tabla
class Tabla(db.Model):
    __tablename__ = "flash_crash_sql"
    id = db.Column(db.Integer, primary_key=True)
    cripto= db.Column(db.String)
    tiempo = db.Column(db.DateTime)
    precio = db.Column(db.Integer)
    s_p = db.Column(db.Integer)
    
    def __repr__(self):
        return f"El precio de {self.cripto} es de {self.precio} dolares"


    # Crear nueva fila
def insert(cripto, tiempo, precio, s_p):
    row = Tabla(cripto= cripto, tiempo= tiempo, precio= precio, s_p= s_p)
    db.session.add(row)             # Agregar nueva fila a la DB
    db.session.commit()


    # Cargar las listas(cripto, tiempo, precio, s_p) en la BD
def lists_to_db(cripto, tiempo, precio, s_p):
    for row in range(len(precio)):
        insert(cripto, tiempo[row], precio[row], s_p[row])
    return()


    # Cargar las listas(cripto, tiempo, precio, s_p) desde la BD
def db_to_lists():
    cripto= []
    tiempo= []
    precio= []
    s_p= []
    query = db.session.query(Tabla) # Traer todos los elementos de la BD
    for row in query:
        cripto.append(row.cripto)
        tiempo.append(row.tiempo)
        precio.append(row.precio)
        s_p.append(row.s_p)
    return(cripto, tiempo, precio, s_p)

