from __future__ import print_function
from bd import obtener_conexion
from __main__ import app
from flask import escape
import sys

def insertar_libro(titulo, descripcion, precio, imagen):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO libros(titulo, descripcion, precio, imagen) VALUES (%s, %s, %s,%s)", (titulo, descripcion, precio,imagen))
            if cursor.rowcount == 1:
                ret={"status": "OK" }
            else:
                ret = {"status": "Failure" }
        code=200
        conexion.commit()
        conexion.close()
    except:
        app.logger.info("Excepcion al insertar un libro")
        ret = {"status": "Failure" }
        code=500
    return ret,code

def convertir_libro_a_json(libro):
    d = {}
    d['id'] = escape(libro[0])
    d['titulo'] = escape(libro[1])
    d['descripcion'] = escape(libro[2])
    d['precio'] = escape(libro[3])
    d['imagen'] = escape(libro[4])
    return d

def obtener_libros():
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, titulo, descripcion, precio,imagen FROM libros")
            libros = cursor.fetchall()
            librosjson=[]
            if libros:
                for libro in libros:
                    librosjson.append(convertir_libro_a_json(libro))
        conexion.close()
        code=200
    except:
        print("Excepcion al obtener los libros", file=sys.stdout)
        librosjson=[]
        code=500
    return librosjson,code

def obtener_libro_por_id(id):
    librojson = {}
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, titulo, descripcion, precio,imagen FROM libros WHERE id = %s", (id,))
            libro = cursor.fetchone()
            if libro is not None:
                librojson = convertir_libro_a_json(libro)
        conexion.close()
        code=200
    except:
        print("Excepcion al recuperar un libro", file=sys.stdout)
        code=500
    return librojson,code


def eliminar_libro(id):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM libros WHERE id = %s", (id,))
            if cursor.rowcount == 1:
                ret={"status": "OK" }
            else:
                ret={"status": "Failure" }
        conexion.commit()
        conexion.close()
        code=200
    except:
        print("Excepcion al eliminar un libro", file=sys.stdout)
        ret = {"status": "Failure" }
        code=500
    return ret,code

def actualizar_libro(id, titulo, descripcion, precio, imagen):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("UPDATE libros SET titulo = %s, descripcion = %s, precio = %s, imagen=%s WHERE id = %s",
                       (titulo, descripcion, precio, imagen,id))
            if cursor.rowcount == 1:
                ret={"status": "OK" }
            else:
                ret={"status": "Failure" }
        conexion.commit()
        conexion.close()
        code=200
    except:
        print("Excepcion al eliminar un libro", file=sys.stdout)
        ret = {"status": "Failure" }
        code=500
    return ret,code
