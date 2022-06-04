import pymongo
from pymongo import MongoClient
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

opcion=int(input("Menú de opciones:\n 1: Listar recolectas \n 2: Crear recolecta \n 3: Modificar recolecta \n 4: Eliminar recolecta \n 5: Listar producciones \n \n Su opción: "))
if opcion==1:
    for recolecta in ListarRecolecta():
        print("=================")
        print("Id Recolecta: ", recolecta["ID_Recolecta"])
        print("Fecha: ", recolecta["Fecha"])
        print("Calidad: ", recolecta["Calidad"])   
        print("Peso: ", recolecta["Peso"]) 
        print("Id Arbol: ", recolecta["ID_Arbol"])   
        print("Id Trabajador: ", recolecta["ID_Trabajador"]) 
        print("Id Produccion: ", recolecta["ID_Produccion"])                                 
elif opcion==2:
    Fecha=input("Ingrese la fecha: ")
    Calidad=input("Ingrese la calidad: ")  
    Peso=input("Ingrese el peso: ")     
    ID_Arbol=input("Ingrese el id del árbol: ")      
    ID_Trabajador=input("Ingrese el id del trabajador: ")
    ID_Produccion=input("Ingrese el id de la produccion: ") 
    ID_Nueva=CrearRecolecta(Fecha,Calidad,Peso,ID_Arbol,ID_Trabajador,ID_Produccion)
    print("El ID de la nueva recolecta es: ",ID_Nueva) 
elif opcion==3:
    ID_Recolecta=int(input("Ingrese el ID de la recolecta a actualizar "))
    Fecha=input("Ingrese la fecha: ")
    Calidad=input("Ingrese la calidad: ")  
    Peso=input("Ingrese el peso: ")     
    ID_Arbol=input("Ingrese el id del árbol: ")      
    ID_Trabajador=input("Ingrese el id del trabajador: ")
    ID_Produccion=input("Ingrese el id de la produccion: ")
    RecolectaActualizada=ModificarRecolecta(ID_Recolecta,Fecha,Calidad,Peso,ID_Arbol,ID_Trabajador,ID_Produccion)
    print("Se han actualizado ",RecolectaActualizada," Recolecta(s) con id",ID_Recolecta) 
elif opcion==4:
    ID_Recolecta=int(input("Ingrese el ID de la recolecta a eliminar "))     
    RecolectaEliminada=EliminarRecolecta(ID_Recolecta)   
    print("Se han eliminado ",RecolectaEliminada," Recolecta(s) con id ",ID_Recolecta)           
elif opcion==5:
    for produccion in ListarProduccion():
        print("=================")
        print("Id produccion: ", produccion["ID_Produccion"])
        print("Fecha: ", produccion["Fecha"])

    


           