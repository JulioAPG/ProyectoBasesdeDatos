from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['[Aguacates]']
Arbol=db.Arbol
Dianostico=db.Diagnostico
Enfermedad=db.Enfermedad
Fumiga=db.Fumiga
Nutre=db.Nutre
Produccion=db.Produccion
Recolecta=db.Recolecta
Trabajador=db.Trabajador
#Pequeña prueba de un read de todos los árboles
cursor = Arbol.find({})
for arbol in cursor:
    print(arbol)