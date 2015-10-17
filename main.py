import tlf
import MySQLdb
import time

try:
    db = MySQLdb.connect("localhost", "root", "Darkgo13", "celulares")
    cursor = db.cursor()
except MySQLdb.Error, e:
    print "Ocurrio un error de conexion: ", e[1]

rep_menu = True


# Opcion 1
def crear_orden():
    # Creando objetos telefonos y asignando a la base de datos
    salir = False
    while not salir:
        tl = tlf.Telefono()
        cursor.execute("SELECT norden FROM orden")
        num_orden = cursor.lastrowid + 1
        print "Numero de Orden !~ ", num_orden, " ~!"
        # Pidiendo los datos del telefono:
        # fec = raw_input("Indique la fecha de ingreso dd-MM-yy: ")
        fec = time.strftime("%d-%m-%Y")
        mrc = raw_input("Indique marca del telefono: ")
        mod = raw_input("Indique modelo del telefono: ")
        ime = raw_input("Indique el imei del telefono: ")
        fal = raw_input("Indique la falla del telefono: ")
        # Asignando los datos a las variables del objeto
        tl.setFecha(fec)
        tl.setMarca(mrc)
        tl.setModelo(mod)
        tl.setImei(ime)
        tl.setFalla(fal)
        tl.setStatus("Pendiente")
        while True:
            print "Datos completados desea salir(s) o crear nueva orden(n): "
            resp = raw_input()
            if resp.lower() == "s":
                try:
                    cursor.execute('''INSERT INTO orden (fecha,marca,modelo,imei,falla)
                                    VALUES (%s,%s,%s,%s,%s)''', (tl.getFecha(), tl.getMarca(), tl.getModelo(),
                                                                 tl.getImei(), tl.getFalla(), tl.getStatus()))
                    db.commit()
                    print "Orden guardada con exito!!"
                except MySQLdb.IntegrityError:
                    print "Error al insertar los valores!!"
                except MySQLdb.Error, e:
                    print "Algo sucedio y no se puede establecer conexion con la base de datos. %d", e[0]
                    print e[1]
                    db.rollback()
                salir = True
                break
            elif resp.lower() == "n":
                try:
                    cursor.execute('''INSERT INTO orden (fecha,marca,modelo,imei,falla)
                                    VALUES (%s,%s,%s,%s,%s)''', (tl.getFecha(), tl.getMarca(), tl.getModelo(),
                                                                 tl.getImei(), tl.getFalla()))
                    db.commit()
                    print "Orden guardada con exito!!"
                    break
                except MySQLdb.IntegrityError:
                    print "Error al insertar los valores!!"
                except MySQLdb.Error, e:
                    print "Algo sucedio y no se puede establecer conexion con la base de datos: ", e[1]
                    db.rollback()
                break
            else:
                print "Opcion incorrecta!!"


# Opcion 2
# Modificar los datos de una orden
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
                print "Opcion incorrecta"


# Mostrar una orden especifica
def mostrar_orden(n_orden):
    try:
        rows_affected = cursor.execute("SELECT * FROM orden WHERE norden=%s", n_orden)
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
                print "****************DATOS ACTUALES DE LA ORDEN***************************"
                print "Numero de Orden: ", norden
                print "Fecha de ingreso: ", fecha
                print "Marca: ", marca
                print "Modelo: ", modelo
                print "IMEI: ", imei
                print "Falla: ", falla
                print "Status: ", estado

        print "***************LLENANDO NUEVOS DATOS***********************"

        fecha = time.strftime("%d-%m-%Y")
        marca = raw_input("Nueva marca: ")
        modelo = raw_input("Nuevo modelo: ")
        imei = raw_input("Nuevo imei: ")
        falla = raw_input("Nueva falla: ")
        estado = raw_input("Nuevo status: ")
        try:
            cursor.execute("UPDATE orden SET fecha=%s, marca=%s, modelo=%s,imei=%s,falla=%s,status=%s WHERE norden=%s",
                           (fecha, marca, modelo, imei, falla, estado, n_orden))
            db.commit()
            print "Orden Actualizada!"
        except MySQLdb.Error, ex:
            print "Error: ", ex[1]
            db.rollback()

        else:
            print "Orden no encontrada verifique e intente nuevamente."
            return False
    except MySQLdb.IntegrityError:
        print "Error en la consulta"
        db.rollback()
        return True
    except MySQLdb.Error, e:
        print "Error: ", e[1]
        db.rollback()
        return True
    return False


# Opcion 3
def eliminar_orden():
    n_orden = raw_input("Indique el numero de la orden que desea eliminar: ")
    try:
        rows_affected = cursor.execute("DELETE FROM orden WHERE norden=%s", n_orden)
        if rows_affected >= 1:
            confirmacion = raw_input("Confirme la eliminacion de la orden? si-no: ")
            db.commit()
            if confirmacion.lower == "si":
                print "Orden Eliminada con exito!"
            else:
                db.rollback()
        else:
            print "No se encontro la orden numero: ", n_orden, " verifique."
    except MySQLdb.Error, e:
        print "Error: ", e[0]
        db.rollback()


# Opcion 4
# Mostrar las ordenes
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
            print "***********************************************************"
            print "Numero de Orden: ", norden
            print "Fecha de ingreso: ", fecha
            print "Marca: ", marca
            print "Modelo: ", modelo
            print "IMEI: ", imei
            print "Falla: ", falla
            print "Status: ", estado
            print "***********************************************************"
        while rep_menu:
            print "\t***********~MENU~*************"
            print "1- Crear Nueva Orden."
            print "2- Modificar Orden."
            print "3- Eliminar Orden."
            print "4- Mostrar Ordenes."
            print "5- Salir del programa."
            opcion = raw_input("Indique su respuesta: ")
            print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
            if opcion == "1":
                crear_orden()
            elif opcion == "2":
                modificar_orden()
            elif opcion == "3":
                eliminar_orden()
            elif opcion == "4":
                mostrar_ordenes()
            elif opcion == "5":
                print "Saliendo del sistema."
                rep_menu = False
                db.close()
                break
            else:
                print "Opcion incorrecta"
                rep_menu = True
