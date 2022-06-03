#Si no cuenta con alguna de estas ñibrerías por favor instalar:

from hmac import trans_36
import pymysql
import json
import stdiomask

print("----------------------------------------------------------------")
print("\nBienvenido al crud del sistema de cajeros \nPrimero necesitamos unos datos: \n")
LocalhhostUser = input("Ingrese el usuario de la base de datos (si es 'root' escriba: si): ")
LocalhhostPass = stdiomask.getpass("Ingrese la contraseña de la base de datos: ")
LocalhhostDB = input("Ingrese el nombre de la base de datos de cajeros como la tenga guardada:\n (si es 'transacciones' escriba: si): ") 
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

n=0
def ConvertirLista(cadena):
    llaves="[]"
    for x in range(len(llaves)):
        cadena = cadena.replace(llaves[x],"")
    cadena=cadena.replace("},","}+")
    lista=list(cadena.split("+"))
    return lista

def CrearCajero(estado, modeloCajero, zona, id_equipo):
    with conexion.cursor() as cursor:
        consulta = "INSERT INTO cajeros(estado, modeloCajero, zona, id_equipo) VALUES (%s, %s, %s, %s);"
        cursor.execute(consulta, (estado, modeloCajero,
                        zona, id_equipo))
    conexion.commit()


def LeerCajero():
    with conexion.cursor() as cursorr:
        cursorr.execute(
            "SELECT estado, modeloCajero, zona, id_equipo FROM cajeros;")
        cajeros = cursorr.fetchall()
        for cajero in cajeros:
            print(cajero)


def EliminarCajero(id_cajero):
    with conexion.cursor() as cursore:
        consulta = "DELETE FROM cajeros WHERE id_equipo=%s;"
        cursore.execute(consulta, (id_cajero))
    conexion.commit()


def ModificarCajero(estado, modelo, zona, id_cajero):
    with conexion.cursor() as cursorm:
        consulta = "UPDATE cajeros SET estado=%s, modeloCajero=%s, zona=%s WHERE id_equipo=%s"
        cursorm.execute(consulta, (estado, modelo, zona, id_cajero))
    conexion.commit()


def LeerTransacciones(id_cajero):
    with conexion.cursor() as cursorr:
        consulta = ("SELECT transacciones FROM cajeros WHERE id_equipo=%s;")
        cursorr.execute(consulta, (id_cajero))
        cajeros = cursorr.fetchall()
        str_cajeros = json.dumps(cajeros)
        objeto_cajeros = json.loads(str_cajeros)
        cajero=objeto_cajeros[0]
        transacciones=cajero[0]
        listaT=ConvertirLista(transacciones)
        return listaT

def EliminarTransaccion(listaTransacciones,numeroTransaccion,id_cajero):
    listaTransacciones.pop(numeroTransaccion-1)
    listaTransacciones=str(listaTransacciones)
    listaTransacciones=listaTransacciones.replace("'","")
    with conexion.cursor() as cursor:
        consulta = "UPDATE cajeros SET transacciones=%s WHERE id_equipo=%s;"
        cursor.execute(consulta, (listaTransacciones,id_cajero))
    conexion.commit() 

def CrearTransaccion(listaT,id_cajero,monto,tipocuenta,tipomovimiento,fechamovimiento):
    NuevaTransaccion='{"monto": %s, "tipoCuenta": "%s","tipoMovimiento": "%s","fechamovimiento": "%s"}' % (monto,tipocuenta,tipomovimiento,fechamovimiento)    
    listaT.append(NuevaTransaccion)
    listaT=str(listaT)
    listaT=listaT.replace("'","")
    with conexion.cursor() as cursorm:
        consulta = "UPDATE cajeros SET transacciones=%s WHERE id_equipo=%s"
        cursorm.execute(consulta, (listaT, id_cajero))
    conexion.commit() 

def ActualizarTransaccion(listaT,id_cajero,monto,tipocuenta,tipomovimiento,fechamovimiento,numeroT):
    NuevaTransaccion='{"monto": %s, "tipoCuenta": "%s","tipoMovimiento": "%s","fechamovimiento": "%s"}' % (monto,tipocuenta,tipomovimiento,fechamovimiento)    
    listaT.pop(numeroT-1)
    listaT.insert(numeroT-1,NuevaTransaccion)
    listaT=str(listaT)
    listaT=listaT.replace("'","")
    with conexion.cursor() as cursorm:
        consulta = "UPDATE cajeros SET transacciones=%s WHERE id_equipo=%s"
        cursorm.execute(consulta, (listaT, id_cajero))
    conexion.commit()  

def RevisarID(id_cajero):
    with conexion.cursor() as cursor:
        consulta = "SELECT id_equipo FROM cajeros WHERE id_equipo=%s;"
        cursor.execute(consulta, (id_cajero))
        cajeros = cursor.fetchall()
        if len(cajeros)==0:
            return False
        else:
            str_cajeros = json.dumps(cajeros)
            objeto_cajeros = json.loads(str_cajeros)
            cajero=objeto_cajeros[0]
            id_cajero=cajero[0]
            return id_cajero

opcion = int(input("¿Que acción desea realizar?: \n 1: Crear cajero \n 2: Visualizar los cajeros \n 3: Eliminar un cajero \n 4: Modificar un cajero \n 5: Ver todas las transacciones de un cajero \n 6: Salir \n Su opción: "))
if opcion == 1:
    print("\n----------------------------------------------------------------\n Creación de cajero: \n")
    CrearCajero("Disponible", 2015,
                 8, "GJHGDJH")
    print(bcolors.OK+'Cajero creado con éxito'+bcolors.RESET)
    print("\n----------------------------------------------------------------\n")
elif opcion == 2:
    print("\n----------------------------------------------------------------\n Cajeros actuales: \n")
    LeerCajero()
    print("\n----------------------------------------------------------------\n")
elif opcion == 3:
    print("\n----------------------------------------------------------------\n Eliminación de cajero: \n")
    id_cajero = input("Digite el id del cajero a eliminar: ")
    RevisarID(id_cajero)
    if RevisarID(id_cajero)==False:
        print(bcolors.FAIL+"El cajero no existe\n---------------------------------------------------------------- \n"+bcolors.RESET)
    else:
        EliminarCajero(id_cajero)
        print(f'El cajero con id {id_cajero} ha sido eliminado exitosamente')
        print("\n----------------------------------------------------------------\n")
elif opcion == 4:
    print("\n----------------------------------------------------------------\n Modificación del cajero: \n")
    id_cajero = input("Digite el id del cajero a modificar: ")
    RevisarID(id_cajero)
    if RevisarID(id_cajero)==False:
        print(bcolors.FAIL+"El cajero no existe\n---------------------------------------------------------------- \n"+bcolors.RESET)
    else:
        estado = input("Digite el nuevo estado: ")
        modelo = input("Digite el nuevo modelo: ")
        zona = input("Digite la nueva zona: ")
        ModificarCajero(estado, modelo, zona, id_cajero)
        print("\n----------------------------------------------------------------\n")
elif opcion == 5:
    print("\n----------------------------------------------------------------\n Transacciones cajero: \n")
    id_cajero = input("Digite el id del cajero a consultar: ")
    RevisarID(id_cajero)
    if RevisarID(id_cajero)==False:
        print(bcolors.FAIL+"El cajero no existe\n---------------------------------------------------------------- \n"+bcolors.RESET)
    else:
        listaT=LeerTransacciones(id_cajero)
        for transaccion in listaT:
            n=n+1
            transaccionJSON=json.loads(transaccion)
            print(f'Transacción {n}',str(transaccionJSON))
        print("\n----------------------------------------------------------------\n")
        n=0
        opcionT = int(input("¿Que acción desea realizar?:\n 1: Crear transacción \n 2: Actualizar transacción \n 3: Eliminar transacción \n 4: Cancelar \n Su opción: "))
        if opcionT==1:
            monto=input("Digite el monto de la nueva transacción: ")
            tipoCuenta=input("Digite el tipo de cuenta: ")
            tipoMovimiento=input("Digite el tipo de movimiento: ")
            fechaMovimiento=input("Digite la fecha del nuevo movimiento en formato D-M-A: ")
            CrearTransaccion(listaT,id_cajero,monto,tipoCuenta,tipoMovimiento,fechaMovimiento)
            listaT=LeerTransacciones(id_cajero)
            for transaccion in listaT:
                n=n+1
                transaccionJSON=json.loads(transaccion)
                print(f'Transacción {n}',str(transaccionJSON))

        if opcionT==2:
            NumeroTransaccion=int(input("Digite el número de la transacción a actualizar:"))
            monto=input("Digite el monto: ")
            tipoCuenta=input("Digite el tipo de cuenta: ")
            tipoMovimiento=input("Digite el tipo de movimiento: ")
            fechaMovimiento=input("Digite la fecha en formato D-M-A: ")
            ActualizarTransaccion(listaT,id_cajero,monto,tipoCuenta,tipoMovimiento,fechaMovimiento,NumeroTransaccion)
            listaT=LeerTransacciones(id_cajero)
            for transaccion in listaT:
                n=n+1
                transaccionJSON=json.loads(transaccion)
                print(f'Transacción {n}',str(transaccionJSON))

        if opcionT==3:
            NumeroTransaccion=int(input("Digite el número de la transacción a eliminar:\n "))
            EliminarTransaccion(listaT,NumeroTransaccion,id_cajero)
            listaT=LeerTransacciones(id_cajero)
            for transaccion in listaT:
                n=n+1
                transaccionJSON=json.loads(transaccion)
                print(f'Transacción {n}',str(transaccionJSON))

        if opcionT==4:
            print("\nAdiós\n----------------------------------------------------------------\n")

elif opcion == 6:
    print("\nAdiós\n----------------------------------------------------------------\n")

else:
    print("\n----------------------------------------------------------------\n Opción inválida \n")
    print("\n----------------------------------------------------------------\n")



