import pymysql
try:
	conexion = pymysql.connect(host='localhost',
                             user='root',
                             password='TraHEY2356!',
                             db='transacciones')
except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
	print("Ocurrió un error al conectar: ", e)        
def CrearCajero(estado,modeloCajero,transacciones,zona,id_equipo):
	with conexion.cursor() as cursor:
		consulta = "INSERT INTO cajeros(estado, modeloCajero, transacciones, zona, id_equipo) VALUES (%s, %s, %s, %s, %s);"
		cursor.execute(consulta, (estado, modeloCajero, transacciones,zona,id_equipo))
	conexion.commit()
def LeerCajero():
	with conexion.cursor() as cursorr:
		cursorr.execute("SELECT estado, modeloCajero, zona, id_equipo FROM cajeros;")
		cajeros = cursorr.fetchall()
		for cajero in cajeros:
			print(cajero)
def EliminarCajero(id_cajero):
	with conexion.cursor() as cursore:
		consulta = "DELETE FROM cajeros WHERE id_equipo=%s;"
		cursore.execute(consulta, (id_cajero))
	conexion.commit()    
def ModificarCajero(estado,modelo,zona,id_cajero):
	with conexion.cursor() as cursorm:
		consulta = "UPDATE cajeros SET estado=%s, modeloCajero=%s, zona=%s WHERE id_equipo=%s"
		cursorm.execute(consulta, (estado,modelo,zona,id_cajero))
	conexion.commit()
def LeerTransacciones(id_cajero):
	with conexion.cursor() as cursorr:
		consulta=("SELECT transacciones FROM cajeros WHERE id_equipo=%s;")
		cursorr.execute(consulta,(id_cajero))
		cajeros = cursorr.fetchall()
		for cajero in cajeros:
			print(cajero)		    		        
opcion=int(input("¿Que acción desea realizar?: \n 1: Crear cajero \n 2:Visualizar los cajeros \n 3:Eliminar un cajero \n 4: Modificar un cajero \n 5: ver todas las transacciones de un cajero \n Su opción: "))
if opcion==1:
    CrearCajero("Disponible",2015,'[{"monto": 10000,"tipoCuenta":"cuentaVirtual","tipoMovimiento":"retiro","fechaMovimiento":"17-06-2022"}]',8,"GJHGDJH")
elif opcion==2:
    LeerCajero()
elif opcion==3:
    id_cajero=input("Digite el id del cajero a eliminar: ")
    EliminarCajero(id_cajero)
elif opcion==4:
    id_cajero=input("Digite el id del cajero a modificar: ")
    estado=input("Digite el nuevo estado: ")
    modelo=input("Digite el nuevo modelo: ")	
    zona=input("Digite la nueva zona: ")				
    ModificarCajero(estado,modelo,zona,id_cajero) 
elif opcion==5:
    id_cajero=input("Digite el id del cajero a consultar: ")
    LeerTransacciones(id_cajero)	
	   


