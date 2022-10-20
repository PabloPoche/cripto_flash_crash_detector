'''
export_csv.py
Contiene las funciones encargadas crear y administrar el archivo flash_crash.csv

- crear_csv:    Crear un nuevo archivo .csv (sobre escribe el anterior)
- write_csv:    Insertar una nueva fila en el archivo .csv
- lists_to_csv: Cargar las listas a las columnas del archivo .csv

'''

import csv


    # Crear un nuevo archivo flash_crash.csv
def crear_csv():
    file= "flash_crash.csv"                         # Nombre del archivo
    header= ["cripto", "tiempo", "precio", "s_p"]   # Nombre de las columnas
    csvfile= open(file, "w", newline="")            # w= sobre escribir(nuevo archivo)
    writer= csv.DictWriter(csvfile, fieldnames= header)
    writer.writeheader() 
    csvfile.close()
    return()


    # Insertar una nueva fila en el archivo flash_crash.csv
def write_csv(row):
    file= "flash_crash.csv"                         # Nombre del archivo
    header= ["cripto", "tiempo", "precio", "s_p"]   # Nombre de las columnas
    csvfile= open(file, "a", newline="")
    writer= csv.DictWriter(csvfile, fieldnames= header)
    writer.writerow(row)
    csvfile.close()
    return()


    # Cargar las listas (cripto, tiempo, precio, s_p) en las columnas del archivo flash_crash.csv
def lists_to_csv(cripto, tiempo, precio, s_p):
    crear_csv()                                     # nuevo archivo .csv (sobre escribe el anterior)
    for x in range(len(cripto)):
        row = {"cripto": cripto[x], "tiempo": tiempo[x], "precio": precio[x], "s_p": s_p[x]}    # fila a escribir
        write_csv(row)
    return()


