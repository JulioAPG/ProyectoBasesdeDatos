#Autores Kevin Alejandro Betancurt, Juan Sebastián Vélez Hernández, Julio Peñaloza
import pymongo
from pymongo import MongoClient

class bcolors:
    OK = '\033[92m'  # GREEN
    WARNING = '\033[93m'  # YELLOW
    FAIL = '\033[91m'  # RED
    RESET = '\033[0m'  # RESET COLOR
    BLUE = '\033[94m'  # BLUE


print(bcolors.OK+"Bienvenido al CRUD no relacional de la base de datos de recoleccion de arboles de aguacates \n")
print("Primero asegurese de haber importado la base de datos en su sitema MongoDB, sin esto el CRUD no funcionará \n"+bcolors.RESET)


def Conectar():
    client = MongoClient('mongodb://localhost:27017/')
    return client['[Aguacates]']

def ListarProduccion():
    db = Conectar()
    return db.Produccion.find() 

def ListarRecolecta():
    db=Conectar()
    return db.Recolecta.find()  

def CrearRecolecta(fecha,calidad,peso,id_arbol,id_trabajador,id_produccion):
    db=Conectar()  
    recolectas = db.Recolecta
    ultimo=db.Recolecta.count_documents({})
    return recolectas.insert_one({
        "ID_Recolecta":ultimo+1,
        "Fecha": fecha,
        "Calidad": calidad,
        "Peso": peso,
        "ID_Arbol":id_arbol,
        "ID_Trabajador":id_trabajador,
        "ID_Produccion":id_produccion
        }).inserted_id      

def ModificarRecolecta(id_recolecta,fecha,calidad,peso,id_arbol,id_trabajador,id_produccion):
    db=Conectar()
    resultado=db.Recolecta.update_one(
        {
            'ID_Recolecta':id_recolecta
        },
        {
            '$set':{
                "ID_Recolecta":id_recolecta,
                "Fecha": fecha,
                "Calidad": calidad,
                "Peso": peso,
                "ID_Arbol":id_arbol,
                "ID_Trabajador":id_trabajador,
                "ID_Produccion":id_produccion                
            }
        }
    )
    return resultado.modified_count

def EliminarRecolecta(id_recolecta):
    db=Conectar()
    resultado=db.Recolecta.delete_one(
        {
            'ID_Recolecta':id_recolecta
        }
    ) 
    return resultado.deleted_count   

def RecolectaArbol():
    # ¿Cuanto se ha recolectado (peso total) de un arbol ingresado (id)?
    ID_Arbol=int(input("Ingrese el id del árbol: ") )
    db=Conectar()
    resultado=db.Recolecta.find({"ID_Arbol":ID_Arbol})
    peso=0
    for recolecta in resultado:
        peso+=recolecta["Peso"]
    print(f"El peso total recolectado del árbol {ID_Arbol} es: ",peso, "kg de aguacate")

def RecolectasTrabajador():
    # ¿Cuantas recolectas ha realizado cada trabajador?
    opcion = int(input("¿Que desea ver? \n 1: Un trabajador especifico \n 2: Todos los trabajadores \n \n Su opción: "))
    if opcion == 1:
        ID_Trabajador=int(input("Ingrese el id del trabajador: ") )
        db=Conectar()
        resultado=db.Recolecta.find({"ID_Trabajador":ID_Trabajador})
        cantidad=0
        for recolecta in resultado:
            cantidad+=1
        print(f"El trabajador {ID_Trabajador} ha realizado {cantidad} recolectas")
    elif opcion == 2:
        db=Conectar()
        ID_Trabajador=0
        for i in range(1,21):
            cantidad = 0
            ID_Trabajador=i
            resultado=db.Recolecta.find({"ID_Trabajador":ID_Trabajador})
            for recolecta in resultado:
                cantidad += 1
            print(f"El trabajador {recolecta['ID_Trabajador']} ha realizado {cantidad} recolectas")
    else:
        print("Opcion no valida")

def ArbolMasRecolectado():
    #¿A qué árbol se le han realizado más recolectas? 
    db=Conectar()
    arboles=db.Arbol.find()
    cantidadtotal=0
    for arbol in arboles: 
        cantidad=db.Recolecta.count_documents({"ID_Arbol": arbol["ID_Arbol"]})
        if cantidad > cantidadtotal:
            ArbolRes=arbol["ID_Arbol"]
            cantidadtotal=cantidad
        elif cantidadtotal == cantidad:
            pass
    print(f"El arbol con mas recolectas es el {ArbolRes} con {cantidadtotal} recolectas")




def main():
    opcion=int(input("Menú de opciones:\n 1: Listar recolectas \n 2: Crear recolecta \n 3: Modificar recolecta \n 4: Eliminar recolecta \n 5: Listar producciones \n 6: Ver el peso recolectado de un árbol \n 7: Ver las recolectas de los trabajadores \n 8: Ver el árbol con más recolectas \n 9: Salir \n \n Su opción: "))
    if opcion==1:
        print("\n----------------------------------------------------------------\n Lista de recolectas: \n")
        for recolecta in ListarRecolecta():
            print("=================")
            print("Id Recolecta: ", recolecta["ID_Recolecta"])
            print("Fecha: ", recolecta["Fecha"])
            print("Calidad: ", recolecta["Calidad"])   
            print("Peso: ", recolecta["Peso"]) 
            print("Id Arbol: ", recolecta["ID_Arbol"])   
            print("Id Trabajador: ", recolecta["ID_Trabajador"]) 
            print("Id Produccion: ", recolecta["ID_Produccion"])   
        print("\n----------------------------------------------------------------\n") 
        main()

    elif opcion==2:
        print("\n----------------------------------------------------------------\n Creación de recolecta: \n")
        Fecha=input("Ingrese la fecha (Año - Mes - Dia): ")
        Calidad=int(input("Ingrese la calidad: \n 1: Alta \n 2: Media \n 3: Baja \n Su opción: "))
        if Calidad==1:
            Calidad="Alta"
        elif Calidad==2:
            Calidad="Media"
        elif Calidad==3:
            Calidad="Baja"
        Peso=int(input("Ingrese el peso: "))   
        ID_Arbol=int(input("Ingrese el id del árbol: ") )     
        ID_Trabajador=input("Ingrese el id del trabajador: ")
        ID_Produccion=input("Ingrese el id de la produccion: ") 
        ID_Nueva=CrearRecolecta(Fecha,Calidad,Peso,ID_Arbol,ID_Trabajador,ID_Produccion)
        db=Conectar()
        ID_NuevoReal=db.Recolecta.find_one({'_id':ID_Nueva},{"_id": False})
        print("La nueva recolecta es: ",ID_NuevoReal) 
        print("\n----------------------------------------------------------------\n")
        main()

    elif opcion==3:
        print("\n----------------------------------------------------------------\n Modificación de recolecta: \n")
        ID_Recolecta=int(input("Ingrese el ID de la recolecta a actualizar: "))
        Fecha=input("Ingrese la fecha: ")
        Calidad=int(input("Ingrese la calidad: \n 1: Alta \n 2: Media \n 3: Baja \n Su opción: "))
        if Calidad==1:
            Calidad="Alta"
        elif Calidad==2:
            Calidad="Media"
        elif Calidad==3:
            Calidad="Baja"
        Peso=input("Ingrese el peso: ")     
        ID_Arbol=input("Ingrese el id del árbol: ")      
        ID_Trabajador=input("Ingrese el id del trabajador: ")
        ID_Produccion=input("Ingrese el id de la produccion: ")
        RecolectaActualizada=ModificarRecolecta(ID_Recolecta,Fecha,Calidad,Peso,ID_Arbol,ID_Trabajador,ID_Produccion)
        print("Se han actualizado ",RecolectaActualizada," Recolecta(s) con id",ID_Recolecta)
        print("\n----------------------------------------------------------------\n") 
        main()

    elif opcion==4:
        print("\n----------------------------------------------------------------\n Eliminación de recolecta: \n")
        ID_Recolecta=int(input("Ingrese el ID de la recolecta a eliminar "))     
        RecolectaEliminada=EliminarRecolecta(ID_Recolecta)   
        print("Se han eliminado ",RecolectaEliminada," Recolecta(s) con id ",ID_Recolecta)    
        print("\n----------------------------------------------------------------\n") 
        main()

    elif opcion==5:
        print("\n----------------------------------------------------------------\n Lista de producciones: \n")
        for produccion in ListarProduccion():
            print("=================")
            print("Id produccion: ", produccion["ID_Produccion"])
            print("Fecha: ", produccion["Fecha"])
        print("\n----------------------------------------------------------------\n")
        main()

    elif opcion==6:
        print("\n----------------------------------------------------------------\n Peso recolectado: \n")
        RecolectaArbol()
        print("\n----------------------------------------------------------------\n")
        main()

    elif opcion==7:
        print("\n----------------------------------------------------------------\n Recolectas de los trabajadores: \n")
        RecolectasTrabajador()
        print("\n----------------------------------------------------------------\n")
        main()

    elif opcion == 8:
        print("\n----------------------------------------------------------------\n Arbol mas recolectado: \n")
        ArbolMasRecolectado()
        print("\n----------------------------------------------------------------\n")
        main()

    elif opcion == 9:
        print("\n Adiós \n----------------------------------------------------------------\n")
        exit()

if __name__ == "__main__":
    main()

    


           