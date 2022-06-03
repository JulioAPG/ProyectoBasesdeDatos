# Si no cuenta con alguna de estas librerías por favor instalar:
import pymysql
import json
import stdiomask

print("----------------------------------------------------------------")
print("\nBienvenido al crud del sistema de cajeros \nPrimero necesitamos unos datos: \n")
LocalhhostUser = input(
    "Ingrese el usuario de la base de datos (si es 'root' escriba: si): ")
LocalhhostPass = stdiomask.getpass(
    "Ingrese la contraseña de la base de datos: ")
LocalhhostDB = input(
    "Ingrese el nombre de la base de datos de cajeros como la tenga guardada:\n (si es 'transacciones' escriba: si): ")
if LocalhhostUser == "si":
    LocalhhostUser = "root"
if LocalhhostDB == "si":
    LocalhhostDB = "transacciones"
print("\n----------------------------------------------------------------\n")


class bcolors:
    OK = '\033[92m'  # GREEN
    WARNING = '\033[93m'  # YELLOW
    FAIL = '\033[91m'  # RED
    RESET = '\033[0m'  # RESET COLOR
    BLUE = '\033[94m'  # BLUE


try:
    conexion = pymysql.connect(host='localhost',
                               user=LocalhhostUser,
                               password=LocalhhostPass,
                               db=LocalhhostDB)
    print(bcolors.OK + "Conexion exitosa :D \n" + bcolors.RESET)
except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
    print(bcolors.FAIL + "Ocurrió un error al conectar:")
    print(e, bcolors.RESET)
    exit()

n = 0


def ConvertirLista(cadena):
    llaves = "[]"
    for x in range(len(llaves)):
        cadena = cadena.replace(llaves[x], "")
    cadena = cadena.replace("},", "}+")
    lista = list(cadena.split("+"))
    return lista


def CrearCajero(estado, modeloCajero, zona, id_equipo):
    #Registrar cajero
    with conexion.cursor() as cursor:
        consulta = "INSERT INTO cajeros(estado, modeloCajero, zona, id_equipo) VALUES (%s, %s, %s, %s);"
        cursor.execute(consulta, (estado, modeloCajero,
                                  zona, id_equipo))
    conexion.commit()


def LeerCajero():
    #Listar cajeros
    with conexion.cursor() as cursorr:
        cursorr.execute(
            "SELECT estado, modeloCajero, zona, id_equipo FROM cajeros;")
        cajeros = cursorr.fetchall()
        for cajero in cajeros:
            print(cajero)


def EliminarCajero(id_cajero):
    #eliminar cajero
    with conexion.cursor() as cursore:
        consulta = "DELETE FROM cajeros WHERE id_equipo=%s;"
        cursore.execute(consulta, (id_cajero))
    conexion.commit()


def ModificarCajero(estado, modelo, zona, id_cajero):
    #Modificar cajero
    with conexion.cursor() as cursorm:
        consulta = "UPDATE cajeros SET estado=%s, modeloCajero=%s, zona=%s WHERE id_equipo=%s"
        cursorm.execute(consulta, (estado, modelo, zona, id_cajero))
    conexion.commit()


def LeerTransacciones(id_cajero):
    #Listar transacciones de un cajero
    with conexion.cursor() as cursorr:
        consulta = ("SELECT transacciones FROM cajeros WHERE id_equipo=%s;")
        cursorr.execute(consulta, (id_cajero))
        cajeros = cursorr.fetchall()
        str_cajeros = json.dumps(cajeros)
        objeto_cajeros = json.loads(str_cajeros)
        cajero = objeto_cajeros[0]
        transacciones = cajero[0]
        listaT = ConvertirLista(transacciones)
        return listaT


def EliminarTransaccion(listaTransacciones, numeroTransaccion, id_cajero):
    #Eliminar transacciones de un cajero
    listaTransacciones.pop(numeroTransaccion-1)
    listaTransacciones = str(listaTransacciones)
    listaTransacciones = listaTransacciones.replace("'", "")
    with conexion.cursor() as cursor:
        consulta = "UPDATE cajeros SET transacciones=%s WHERE id_equipo=%s;"
        cursor.execute(consulta, (listaTransacciones, id_cajero))
    conexion.commit()


def CrearTransaccion(listaT, id_cajero, monto, tipocuenta, tipomovimiento, fechamovimiento):
    #Registrar transacciones de un cajero
    NuevaTransaccion = '{"monto": %s, "tipoCuenta": "%s","tipoMovimiento": "%s","fechamovimiento": "%s"}' % (
        monto, tipocuenta, tipomovimiento, fechamovimiento)
    listaT.append(NuevaTransaccion)
    listaT = str(listaT)
    listaT = listaT.replace("'", "")
    with conexion.cursor() as cursorm:
        consulta = "UPDATE cajeros SET transacciones=%s WHERE id_equipo=%s"
        cursorm.execute(consulta, (listaT, id_cajero))
    conexion.commit()


def ActualizarTransaccion(listaT, id_cajero, monto, tipocuenta, tipomovimiento, fechamovimiento, numeroT):
    #Modificar transacciones de un cajero
    NuevaTransaccion = '{"monto": %s, "tipoCuenta": "%s","tipoMovimiento": "%s","fechamovimiento": "%s"}' % (
        monto, tipocuenta, tipomovimiento, fechamovimiento)
    listaT.pop(numeroT-1)
    listaT.insert(numeroT-1, NuevaTransaccion)
    listaT = str(listaT)
    listaT = listaT.replace("'", "")
    with conexion.cursor() as cursorm:
        consulta = "UPDATE cajeros SET transacciones=%s WHERE id_equipo=%s"
        cursorm.execute(consulta, (listaT, id_cajero))
    conexion.commit()


def RevisarID(id_cajero):
    with conexion.cursor() as cursor:
        consulta = "SELECT id_equipo FROM cajeros WHERE id_equipo=%s;"
        cursor.execute(consulta, (id_cajero))
        cajeros = cursor.fetchall()
        if len(cajeros) == 0:
            return False
        else:
            str_cajeros = json.dumps(cajeros)
            objeto_cajeros = json.loads(str_cajeros)
            cajero = objeto_cajeros[0]
            id_cajero = cajero[0]
            return id_cajero


def ConsignacionesCajerosFallando():
    # El número de consignaciones en los cajeros que están fallando (Fuera de Servicio y Cerrados).
    # Recaudo total de las consignaciones realizadas en los cajeros que están fallando.
    with conexion.cursor() as cursor:
        consulta = "SELECT id_equipo FROM cajeros WHERE estado='Fuera de Servicio' OR estado='Cerrado';"
        cursor.execute(consulta)
        cajeros = cursor.fetchall()
        str_cajeros = json.dumps(cajeros)
        objeto_cajeros = json.loads(str_cajeros)
        for cajero in objeto_cajeros:
            id_cajero = "".join(cajero)
            listaT = LeerTransacciones(id_cajero)
            print(bcolors.OK+f"\nCajero: {id_cajero}"+bcolors.RESET)
            n = 0
            x = 0
            montoTotal = 0
            for transaccion in listaT:
                n = n+1
                transaccionJSON = json.loads(transaccion)
                if transaccionJSON["tipoMovimiento"] == "consignacion":
                    x = x+1
                    monto = int(transaccionJSON["monto"])
                    montoTotal = montoTotal + monto
                    print("Transaccion", n, ":", "Valor:", transaccionJSON["monto"], " - ", "Tipo de cuenta:", transaccionJSON["tipoCuenta"], " - ",
                          "Tipo de movimento:", transaccionJSON["tipoMovimiento"], " - ", "Fecha de la transaciión:", transaccionJSON["fechaMovimiento"])
            print(bcolors.BLUE+f"Numero de consignaciones: {x}")
            print(f"Recaudo total de consignaciones: {montoTotal}"+ bcolors.RESET)



def main():
    opcion = int(input("¿Que acción desea realizar?: \n 1: Crear cajero \n 2: Visualizar los cajeros \n 3: Eliminar un cajero \n 4: Modificar un cajero \n 5: Editar las transacciones de un cajero \n 6: Ver las transacciones de un cajero \n 7: El número y recaudo total de consignaciones en los cajeros que están fallando \n 8: Salir \n Su opción: "))
    if opcion == 1:
        print("\n----------------------------------------------------------------\n Creación de cajero: \n")
        id_equipo = input("ID del cajero: ")
        RevisarID(id_equipo)
        if RevisarID(id_equipo) == False:
            estado = int(input(
                "Estado del cajero: \n 1: Operando \n 2: Fuera de servicio \n 3: Cerrado \n Opcion: "))
            if estado == 1:
                estado = "Operando"
            elif estado == 2:
                estado = "Fuera de servicio"
            elif estado == 3:
                estado = "Cerrado"
            else:
                print("\n Opcion no valida")
                exit()
            modeloCajero = input("Modelo del cajero: \n Año de fabricación: ")
            zona = int(
                input("Zona del cajero: \n Por favor ingrese un número entre 1 y 10: "))
            CrearCajero(estado, modeloCajero, zona, id_equipo)
            print(bcolors.OK+'\n Cajero creado con éxito \n'+bcolors.RESET)
            main()
        else:
            print(bcolors.FAIL+"\n El cajero ya existe"+bcolors.RESET)
            main()
        print("\n----------------------------------------------------------------\n")

    elif opcion == 2:
        print("\n----------------------------------------------------------------\n Cajeros actuales: \n")
        LeerCajero()
        print("\n----------------------------------------------------------------\n")
        main()
    elif opcion == 3:
        print("\n----------------------------------------------------------------\n Eliminación de cajero: \n")
        id_cajero = input("Digite el id del cajero a eliminar: ")
        RevisarID(id_cajero)
        if RevisarID(id_cajero) == False:
            print(bcolors.FAIL+"El cajero no existe\n---------------------------------------------------------------- \n"+bcolors.RESET)
            main()
        else:
            EliminarCajero(id_cajero)
            print(
                bcolors.OK+f'El cajero con id {id_cajero} ha sido eliminado exitosamente'+bcolors.RESET)
            print("\n----------------------------------------------------------------\n")
            main()
    elif opcion == 4:
        print("\n----------------------------------------------------------------\n Modificación del cajero: \n")
        id_cajero = input("Digite el id del cajero a modificar: ")
        RevisarID(id_cajero)
        if RevisarID(id_cajero) == False:
            print(bcolors.FAIL+"El cajero no existe\n---------------------------------------------------------------- \n"+bcolors.RESET)
            main()
        else:
            estado = int(input(
                "Estado del cajero: \n 1: Operando \n 2: Fuera de servicio \n 3: Cerrado \n Opcion: "))
            if estado == 1:
                estado = "Operando"
            elif estado == 2:
                estado = "Fuera de servicio"
            elif estado == 3:
                estado = "Cerrado"
            else:
                print("\n Opcion no valida")
                main()
            modeloCajero = input("Modelo del cajero: \n Año de fabricación: ")
            zona = int(
                input("Zona del cajero: \n Por favor ingrese un número entre 1 y 10: "))
            ModificarCajero(estado, modeloCajero, zona, id_cajero)
            print(bcolors.OK+'\n Cajero actualizado con éxito \n'+bcolors.RESET)
            main()
    elif opcion == 5:
        n = 0
        print("\n----------------------------------------------------------------\n Transacciones cajero: \n")
        id_cajero = input("Digite el id del cajero a consultar: ")
        RevisarID(id_cajero)
        if RevisarID(id_cajero) == False:
            print(bcolors.FAIL+"El cajero no existe\n---------------------------------------------------------------- \n"+bcolors.RESET)
            main()
        else:
            listaT = LeerTransacciones(id_cajero)
            for transaccion in listaT:
                n = n+1
                transaccionJSON = json.loads(transaccion)
                print(f'Transacción {n}', str(transaccionJSON))
            print("\n----------------------------------------------------------------\n")
            n = 0
            opcionT = int(input(
                "¿Que acción desea realizar?:\n 1: Crear transacción \n 2: Actualizar transacción \n 3: Eliminar transacción \n 4: Cancelar \n Su opción: "))
            if opcionT == 1:
                monto = int(input("Digite el monto de la nueva transacción: "))
                tipoCuenta = input(
                    "Tipo de cuenta: \n 1: Cuenta corriente \n 2: Cuenta de ahorro \n 3: Cuenta virtual \n Su opción: ")
                if tipoCuenta == 1:
                    tipoCuenta = "corriente"
                elif tipoCuenta == 2:
                    tipoCuenta = "ahorro"
                elif tipoCuenta == 3:
                    tipoCuenta = "cuentaVirtual"
                else:
                    print("\n Opcion no válida")
                    main()
                tipoMovimiento = input(
                    "Digite el tipo de movimiento: \n 1: Retiro \n 2: Consignación \n 3: Transferencia \n Su opción: ")
                if tipoMovimiento == 1:
                    tipoMovimiento = "retiro"
                elif tipoMovimiento == 2:
                    tipoMovimiento = "consignacion"
                elif tipoMovimiento == 3:
                    tipoMovimiento = "transferencia"
                else:
                    print("\n Opcion no válida")
                    main()
                fechaMovimiento = input(
                    "Digite la fecha del nuevo movimiento en formato D-M-A: ")
                CrearTransaccion(listaT, id_cajero, monto,
                                 tipoCuenta, tipoMovimiento, fechaMovimiento)
                listaT = LeerTransacciones(id_cajero)
                for transaccion in listaT:
                    n = n+1
                    transaccionJSON = json.loads(transaccion)
                    print(f'Transacción {n}', str(transaccionJSON))

            if opcionT == 2:
                NumeroTransaccion = int(
                    input("Digite el número de la transacción a actualizar:"))
                monto = int(input("Digite el monto: "))
                tipoCuenta = input(
                    "Tipo de cuenta: \n 1: Cuenta corriente \n 2: Cuenta de ahorro \n 3: Cuenta virtual \n Su opción: ")
                if tipoCuenta == 1:
                    tipoCuenta = "corriente"
                elif tipoCuenta == 2:
                    tipoCuenta = "ahorro"
                elif tipoCuenta == 3:
                    tipoCuenta = "cuentaVirtual"
                else:
                    print("\n Opcion no válida")
                    main()
                tipoMovimiento = input(
                    "Digite el tipo de movimiento: \n 1: Retiro \n 2: Consignación \n 3: Transferencia \n Su opción: ")
                if tipoMovimiento == 1:
                    tipoMovimiento = "retiro"
                elif tipoMovimiento == 2:
                    tipoMovimiento = "consignacion"
                elif tipoMovimiento == 3:
                    tipoMovimiento = "transferencia"
                else:
                    print("\n Opcion no válida")
                    main()
                fechaMovimiento = input("Digite la fecha en formato D-M-A: ")
                ActualizarTransaccion(listaT, id_cajero, monto, tipoCuenta,
                                      tipoMovimiento, fechaMovimiento, NumeroTransaccion)
                listaT = LeerTransacciones(id_cajero)
                for transaccion in listaT:
                    n = n+1
                    transaccionJSON = json.loads(transaccion)
                    print(f'Transacción {n}', str(transaccionJSON))

            if opcionT == 3:
                NumeroTransaccion = int(
                    input("Digite el número de la transacción a eliminar:\n "))
                EliminarTransaccion(listaT, NumeroTransaccion, id_cajero)
                listaT = LeerTransacciones(id_cajero)
                for transaccion in listaT:
                    n = n+1
                    transaccionJSON = json.loads(transaccion)
                    print(f'Transacción {n}', str(transaccionJSON))

            if opcionT == 4:
                print(
                    "\nAdiós\n----------------------------------------------------------------\n")
                main()
        main()
    elif opcion == 6:
        n = 0
        print("\n----------------------------------------------------------------\n Transacciones cajero: \n")
        id_cajero = input("Digite el id del cajero a consultar: ")
        RevisarID(id_cajero)
        if RevisarID(id_cajero) == False:
            print(bcolors.FAIL+"El cajero no existe\n---------------------------------------------------------------- \n"+bcolors.RESET)
            main()
        else:
            listaT = LeerTransacciones(id_cajero)
            for transaccion in listaT:
                n = n+1
                transaccionJSON = json.loads(transaccion)
                print(f'Transacción {n}', str(transaccionJSON))
            print("\n----------------------------------------------------------------\n")
            main()

    elif opcion == 7:
        print("----------------------------------------------------------------\n")
        ConsignacionesCajerosFallando()
        print("----------------------------------------------------------------\n")
        main()

    elif opcion == 8:
        print("\nAdiós\n----------------------------------------------------------------\n")

    else:
        print("\n----------------------------------------------------------------\n Opción inválida")
        print("\n----------------------------------------------------------------\n")


if __name__ == "__main__":
    main()
