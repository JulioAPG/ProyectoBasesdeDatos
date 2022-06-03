import pymysql
import json

print("----------------------------------------------------------------")
print("\nBienvenido al crud del sistema de cajeros \nPrimero necesitamos unos datos: \n")
LocalhhostUser = input("Ingrese el usuario de la base de datos: ")
LocalhhostPass = input("Ingrese la contraseña de la base de datos: ")
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
                               db='transacciones')
    print(bcolors.OK + "Conexion exitosa :D \n" + bcolors.RESET)
except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
    print(bcolors.FAIL + "Ocurrió un error al conectar:")
    print(e, bcolors.RESET)
    exit()


# funcion para convertir el json en un diccionario
def jsonDiccionario():
    with conexion.cursor() as cursord:
        cursord.execute("SELECT transacciones FROM cajeros;")
        cajeros = cursord.fetchall()
        str_cajeros = json.dumps(cajeros)
        objeto_cajeros = json.loads(str_cajeros)
        n = 0
        for cajero in objeto_cajeros:
            n = n+1
            print(f'Cajero {n}:\n', cajero)
        print(type(objeto_cajeros))
        print(type(cajeros))


def prueba():
    json_str = r'["Alice", "Bob", "Carl"]'
    print(type(json_str))


    my_tuple = tuple(json.loads(json_str))

    print(my_tuple)  # 👉️ ('Alice', 'Bob', 'Carl')
    print(type(my_tuple))  # 👉️ <class 'tuple'>

    my_json_str = json.dumps(my_tuple)

    print(my_json_str)  # 👉️ '["Alice", "Bob", "Carl"]'
    print(type(my_json_str))  # 👉️ <class 'str'>


def CrearCajero(estado, modeloCajero, transacciones, zona, id_equipo):
    with conexion.cursor() as cursor:
        consulta = "INSERT INTO cajeros(estado, modeloCajero, transacciones, zona, id_equipo) VALUES (%s, %s, %s, %s, %s);"
        cursor.execute(consulta, (estado, modeloCajero,
                       transacciones, zona, id_equipo))
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
        for cajero in cajeros:
            print(cajero)


opcion = int(input("¿Que acción desea realizar?: \n 1: Crear cajero \n 2: Visualizar los cajeros \n 3: Eliminar un cajero \n 4: Modificar un cajero \n 5: Ver todas las transacciones de un cajero \n 6: Cajeros diccioanrio \n \n Su opción: "))
if opcion == 1:
    print("\n----------------------------------------------------------------\n Creación de cajero: \n")
    CrearCajero("Disponible", 2015,
                '[{"monto": 10000,"tipoCuenta":"cuentaVirtual","tipoMovimiento":"retiro","fechaMovimiento":"17-06-2022"}]', 8, "GJHGDJH")
    print("\n----------------------------------------------------------------\n")
elif opcion == 2:
    print("\n----------------------------------------------------------------\n Cajeros actuales: \n")
    LeerCajero()
    print("\n----------------------------------------------------------------\n")
elif opcion == 3:
    print("\n----------------------------------------------------------------\n Eliminación de cajero: \n")
    id_cajero = input("Digite el id del cajero a eliminar: ")
    EliminarCajero(id_cajero)
    print("\n----------------------------------------------------------------\n")
elif opcion == 4:
    print("\n----------------------------------------------------------------\n Modificación del cajero: \n")
    id_cajero = input("Digite el id del cajero a modificar: ")
    estado = input("Digite el nuevo estado: ")
    modelo = input("Digite el nuevo modelo: ")
    zona = input("Digite la nueva zona: ")
    ModificarCajero(estado, modelo, zona, id_cajero)
    print("\n----------------------------------------------------------------\n")
elif opcion == 5:
    print("\n----------------------------------------------------------------\n Transacciones cajero: \n")
    id_cajero = input("Digite el id del cajero a consultar: ")
    LeerTransacciones(id_cajero)
    print("\n----------------------------------------------------------------\n")
elif opcion == 6:
    print("\n----------------------------------------------------------------\n Diccionario json: \n")
    jsonDiccionario()
    print("\n----------------------------------------------------------------\n")
elif opcion == 7:
    print("\n----------------------------------------------------------------\n Prueba: \n")
    prueba()
    print("\n----------------------------------------------------------------\n")
