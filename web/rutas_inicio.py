from __future__ import print_function
from __main__ import app, csrf
from flask import request,session, make_response
from flask_wtf.csrf import generate_csrf
from bd import obtener_conexion
from funciones import cipher_password, compare_password,create_session,delete_session
import json
import sys
import datetime as dt

@app.route("/login",methods=['POST'])
def login():
    content_type = request.headers.get('Content-Type')
    ret={"status":"ERROR"}
    if (content_type == 'application/json'):
        libro_json = request.json
        username = libro_json['username']
        passwordIn = libro_json['password']
        try:
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                 cursor.execute("SELECT perfil,clave,numAccesosErroneos FROM usuarios WHERE estado='activo' and usuario = %s",(username))
                 usuario = cursor.fetchone()
                 if usuario is None:
                    ret = {"status": "ERROR","mensaje":"Usuario/clave erroneo" }
                 else:
                    app.logger.info("Usuario %s clave erronea",username)
                    perfil=usuario[0]
                    password=usuario[1]
                    numAccesosErroneos=usuario[2]
                    estado='activo'

                    current_date = dt.date.today()
                    hoy=current_date.strftime('%Y-%m-%d')
                    
                    if (compare_password(password.encode("utf-8"),passwordIn.encode("utf-8"))):
                        ret = {"status": "OK","csrf_token": generate_csrf()}
                        app.logger.info("clave bien")
                        create_session(username,perfil)
                        numAccesosErroneos=0
                    else:
                        numAccesosErroneos=numAccesosErroneos+1
                        if (numAccesosErroneos>2):
                            estado="bloqueado"
                            app.logger.info("Usuario %s bloqueado",username)
                        ret = {"status": "ERROR","mensaje":"Usuario/clave erroneo"}
                    cursor.execute("UPDATE usuarios SET numAccesosErroneos=%s, fechaUltimoAcceso=%s, estado=%s WHERE usuario = %s",(numAccesosErroneos,hoy,estado,username))
                 conexion.commit()
                 conexion.close()
                 code=200
        except:
            print("Excepcion al validar al usuario")   
            ret={"status":"ERROR"}
            code=500
    else:
        ret={"status":"Bad request"}
        code=401
    response=make_response(json.dumps(ret),code)
    return response

@app.route("/registro",methods=['POST'])
def registro():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        libro_json = request.json
        username = libro_json['username']
        password = libro_json['password']
        try:
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                 cursor.execute("SELECT perfil FROM usuarios WHERE usuario = %s",(username,))
                 usuario = cursor.fetchone()
                 if usuario is None:
                     passwordC=cipher_password(password);
                     cursor.execute("INSERT INTO usuarios(usuario,clave,perfil,estado,numAccesosErroneos) VALUES(%s,%s,'normal','activo',0)",(username,passwordC))
                     if cursor.rowcount == 1:
                         conexion.commit()
                         app.logger.info("Nuevo usuario creado")
                         ret={"status": "OK" }
                         code=200
                     else:
                         ret={"status": "ERROR" }
                         code=500
                 else:
                   ret = {"status": "ERROR","mensaje":"Usuario ya existe" }
                   code=200
            conexion.close()
        except:
            print("Excepcion al registrar al usuario")   
            ret={"status":"ERROR"}
            code=500
    else:
        ret={"status":"Bad request"}
        code=401
    response=make_response(json.dumps(ret),code)
    return response


@app.route("/logout",methods=['GET'])
def logout():
    try:
        delete_session()
        ret={"status":"OK"}
        code=200
    except:
        ret={"status":"ERROR"}
        code=500
    response=make_response(json.dumps(ret),code)
    return response
