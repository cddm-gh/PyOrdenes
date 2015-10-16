__author__ = 'gorydev'
# Version 1.1

import equipo
import MySQLdb
import time
import re

try:
    db = MySQLdb.connect("localhost", "root", "Darkgo13", "celulares")
    cursor = db.cursor()
except MySQLdb.Error, e:
    print("Ocurrio un error al intentar conectar con la BD: ", e[1])

rep_menu = True
# Opcion 1


def pedir_datos():
    # TODO validar los datos de entrada
    valido = False
    reg = re.compile("^[0-9]{1,15}$")
    while not valido:
        while True:
            mrc = raw_input("Indique marca del equipo: ")
            if len(mrc) < 3:
                print "Indique una marca valida"
                valido = False
            else:
                valido = True
                break
        while True:
            mod = raw_input("Indique modelo del equipo: ")
            if len(mod) < 3:
                print "Indique un modelo valido"
                valido = False
            else:
                valido = True
                break
        while True:
            ime = raw_input("Indique imei del equipo: ")
            if not re.match(reg, ime):
                print "Error el IMEI debe ser solo numeros y contener 15 digitos!"
                valido = False
            else:
                valido = True
                break
        while True:
            fal = raw_input("Indique falla del equipo: ")
            if len(fal) < 5:
                print "Por favor especifique mejor la falla"
                valido = False
            else:
                valido = True
                break


def crear_orden():
    salir = False
    while not salir:
        eq = equipo.Equipo()
        cursor.execute("SELECT norden FROM orden")
        # FIXME mostrar el numero de orden que corresponde
        num_orden = cursor.lastrowid + 1
        print "Numero de orden !~ ", num_orden, " ~!"
        fec = time.strftime("%d-%m-%Y")
        pedir_datos()
        # TODO: Buscar como enviar el objeto equipo para llenar sus datos en otra funcion
        eq.setfecha(fec)
        eq.setmarca(mrc)
        eq.setmodelo(mod)
        eq.setimei(ime)
        eq.setfalla(fal)
        eq.setstatus("Pendiente")

        while True:
            print "Datos completados desea salir (s) o crear nueva orden (n) "
            resp = raw_input()
            if resp.lower() == "s":
                try:
                    cursor.execute('''INSERT INTO orden (fecha,marca,modelo,imei,falla,status)
                        VALUES (%s,%s,%s,%s,%s,%s)''',  (eq.getfecha(), eq.getmarca(), eq.getmodelo(),
                                                         eq.getimei(), eq.getfalla(), eq.getstatus()))
                    db.commit()
                    print "Orden guardada con exito!!"
                except MySQLdb.Error, e:
                    print "Error al insertar valores: ", e[1]
                    db.rollback()
                salir = True
                break
            elif resp.lower() == "n":
                try:
                    cursor.execute('''INSERT INTO orden (fecha,marca,modelo,imei,falla,status)
                        VALUES (%s,%s,%s,%s,%s,%s)''', (eq.getfecha(), eq.getmarca(), eq.getmodelo(),
                                                        eq.getimei(), eq.getfalla(), eq.getstatus()))
                    db.commit()
                    print "Orden guardada con exito!!"
                    break
                except MySQLdb.Error, e:
                    print "Error al insertar valores: ", e[1]
                    db.rollback()
                break
            else:
                print "Opcion incorrecta!!"


def modificar_orden():
    salgo = False
    while not salgo:
        n_orden = raw_input("Indique el numero de orden que desea modificar: ")
        salgo = mostrar_orden(n_orden)
        while True:
            resp = raw_input("Quiere modificar otra orden? si-no: ")
            if resp.lower() == "si":
                break
            elif resp.lower() == "no":
                salgo = True
                break
            else:
                print "Opcion incorrecta!"


def mostrar_orden(n_orden):
    try:
        rows_affected = cursor.execute("SELECT * FROM orden WHERE norden=%s",n_orden)
        db.commit()
        if rows_affected >= 1:
            resultados = cursor.fetchall()
            for registro in resultados:
                norden = registro[0]
                fecha = registro[1]
                marca = registro[2]
                modelo = registro[3]
                imei = registro[4]
                falla = registro[5]
                estado = registro[6]
                print "*********************DATOS ACTUALES DE LA ORDEN**********************"
                print "Numero de orden: ", norden
                print "Fecha de ingreso: ", fecha
                print "Marca: ", marca
                print "Modelo: ", modelo
                print "IMEI: ", imei
                print "Falla: ", falla
                print "Status: ", estado
                print "********************LLENANDO NUEVOS DATOS*****************************"
                fecha = time.strftime("%d-%m-%Y")
                marca = raw_input("Nueva marca: ")
                modelo = raw_input("Nuevo modelo: ")
                imei = raw_input("Nuevo imei: ")
                falla = raw_input("Nueva falla: ")
                estado = raw_input("Nuevo status: ")
                try:
                    cursor.execute("UPDATE orden SET fecha=%s, marca=%s, modelo=%s, imei=%s, falla=%s,"
                                   " status=%s WHERE norden=%s", fecha, marca, modelo, imei, falla, estado, n_orden)
                    db.commit()
                    print "Orden Actualizada!"
                except MySQLdb.Error, e:
                    print "Error al actualizar: ", e[1]
                    db.rollback()
        else:
            print "Orden no encontrada verifique e intente nuevamente."
            return False
    except MySQLdb.Error, e:
        print "Error en la consulta: ", e[1]
        db.rollback()
        return True
    return False


def eliminar_orden():
    n_orden = raw_input("Indique el numero de la orden que desea eliminar: ")
    try:
        rows_affected = cursor.execute("DELETE FROM orden WHERE norden=%s", n_orden)
        if rows_affected >= 1:
            confirmacion = raw_input("Confirme la eliminacion de la orden si-no: ")
            if confirmacion.lower() == "si":
                print "Orden eliminada con exito!"
                db.commit()
            else:
                db.rollback()
        else:
            print "No se encontre la orden numero: ", n_orden, " verifique"
    except MySQLdb.Error, e:
        print "Error: ", e[1]
        db.rollback()


def mostrar_ordenes():
    while True:
        cursor.execute("SELECT * FROM orden")
        resultados = cursor.fetchall()
        for registro in resultados:
            norden = registro[0]
            fecha = registro[1]
            marca = registro[2]
            modelo = registro[3]
            imei = registro[4]
            falla = registro[5]
            estado = registro[6]
            print "****************************************************"
            print "Numero de orden: ", norden
            print "Fecha de ingreso: ", fecha
            print "Marca: ", marca
            print "Modelo: ", modelo
            print "IMEI: ", imei
            print "Falla: ", falla
            print "Status: ", estado
            print "****************************************************"
        break


while rep_menu:
    print "********************MENU*************************"
    print "1- Crear nueva orden"
    print "2- Modificar orden"
    print "3- Eliminar orden"
    print "4- Mostrar ordenes"
    print "5- Salir del programa"
    opcion = raw_input("Indique su opcion: ")
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    if opcion == "1":
        crear_orden()
    elif opcion == "2":
        modificar_orden()
    elif opcion == "3":
        eliminar_orden()
    elif opcion == "4":
        mostrar_ordenes()
    elif opcion == "5":
        print "Saliendo del sistema"
        rep_menu = False
        db.close()
        break
    else:
        print "Opcion incorrecta"
        rep_menu = True
