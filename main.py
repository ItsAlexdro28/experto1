import json
import modules.camps as cs
import modules.blueprints as bp
DIR = 'data/'
campus = {}
registration = {}
i = {}

#registrar campers
#3 rutas
#prueba minima, teorica practiva >= 60
#areas entrenar 3, 33
#rutas:
#* Fundamentos de programación (Introducción a la algoritmia, PSeInt y Python)
#* Programación Web (HTML, CSS y Bootstrap)
#* Programación formal (Java, JavaScript, C#)
#* Bases de datos (Mysql, MongoDb y Postgresql). Cada ruta tiene un SGDB principal y un alternativo.
#* Backend (NetCore, Spring Boot, NodeJS y Express)
#asignar campers, no exceder
#entrenadores a diferentes rutas horario
#gestor matriculas, camper aprobado, experto, ruta, inicio final
#2 pruebas, >= 60, teo 30% pract 60%, quiz 10%, fnl > 60
# <60 llamado atencion, riesgo
#
#

def readJson(filename):
    try:
        with open(DIR+filename+'.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{filename}' not found.")
    except json.JSONDecodeError:
        raise json.JSONDecodeError(f"Invalid JSON format in file '{filename}'.")
    
def writeJson(data, filename):
    try:
        with open(DIR+filename+'.json', 'w') as f:
            json.dump(data, f, indent=4) 
    except IOError as e:
        raise IOError(f"Error writing to file '{filename}': {e}")

def blueprint(blueprint, filename):
    try:
        writeJson(blueprint, filename)
        print(f"JSON file '{filename}' created successfully.")
    except IOError as e:
        raise IOError(f"Error creating file '{filename}': {e}")


def mnu():
    global campus
    global registration
    print("""

    CAMPUSLANDS
          
    1. ingresar estudiante
    2. ingresar nuevo trainer
    3. control matriculas
    4. reportes
    5. generar archivos
    6. leer datos
    7. guardar datos
    8. salir

    """)
    match(input()):
        case '1':
            cs.addCamper(campus['campers'])
        case '2':
            cs.addTrainer(campus['trainers'])
        case '3':
            rgstr()
        case '4':
            rprts()
        case '5':
            blueprint(bp.campusBlueprint, 'campus')
            writeJson({}, 'registration')
        case '6':
            campus = readJson('campus')
            registration = readJson('registration')
        case '7':
            writeJson(campus, 'campus')
            writeJson(registration, 'registration')
        case '8':
            exit()
        case '9':
            print(campus)

def rgstr():
    print("""

    CAMPUSLANDS MATRICULAS
          
    1. asignar notas
    2. generar ruta
    3. asignar estudiante a ruta
    4. regresar

    """)
    match(input()):
        case '1':
            cs.assignGrade(campus)
        case '2':
            holder = cs.generateRoute(campus, registration)
            registration.update(holder)
            holder = None
        case '3':
            cs.assignStunt
        case '4':
            mnu()

def rprts():
    print("""

    CAMPUSLANDS REPORTES
          
    1. inscritos
    2. aprovado inicial
    3. trainers
    4. bajo rendimiento
    5. trainers acargo de campers
    6. campers aprobados o no de cada modulo
    7. regresar

    """)
    match(input()):
        case '1':
            cs.inscrit(campus, registration)
        case '2':
            cs.espera(campus, registration)
        case '3':
            cs.trains(campus, registration)
        case '4':
            cs.bajo(campus, registration)
        case '5':
            cs.trainscamps(campus, registration)
        case '6':
            cs.aprove(campus, registration)
        case '7':
            mnu()

    
while True:
    mnu()