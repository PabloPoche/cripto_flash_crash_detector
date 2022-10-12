'''
sql_db.py 
Contiene las funciones encargadas de crear y administrar la DB(flash_crash.db)

- Crear una nueva BD (sobre escribe la anterior)
- insert:         Insertar una nueva fila en la BD
- lists_to_db:    Cargar las listas en la BD
- db_to_lists:    Cargar las listas con la DB

'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()



    # Crea una nueva tabla
class Tabla(db.Model):
    __tablename__ = "flash_crash_sql"
    id = db.Column(db.Integer, primary_key=True)
    cripto= db.Column(db.String)
    precio = db.Column(db.Integer)
    tiempo = db.Column(db.DateTime)
    s_p = db.Column(db.Integer)
    
    def __repr__(self):
        return f"El precio de {self.cripto} es de {self.precio} dolares"


    # Crear nueva fila
def insert(cripto, precio, tiempo, s_p):
    row = Tabla(cripto= cripto, precio= precio, tiempo= tiempo, s_p= s_p)
    db.session.add(row)             # Agregar nueva fila a la DB
    db.session.commit()


    # Cargar las listas(cripto, precio, tiempo, s_p) en la BD
def lists_to_db(cripto, precio, tiempo, s_p):
    for row in range(len(precio)):
        insert(cripto, precio[row], tiempo[row], s_p[row])
    return()


    # Cargar las listas(cripto, precio, tiempo, s_p) desde la BD
def db_to_lists():
    cripto= []
    precio= []
    tiempo= []
    s_p= []
    query = db.session.query(Tabla) # Traer todos los elementos de la BD
    for row in query:
        cripto.append(row.cripto)
        precio.append(row.precio)
        tiempo.append(row.tiempo)
        s_p.append(row.s_p)
    return(cripto, precio, tiempo, s_p)


