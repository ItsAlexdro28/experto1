y = 1
def addCamper(campers:dict):
    id = input('Ingrese ID: ')
    nombre = input('Ingrese nombre: ')
    apellido = input('Ingrese apelido: ')
    direccion = input('Ingrese direccion: ')
    state = 'Inscrito'
    tel = input('Ingrese telefono: ')
    camper = {
        'id':id,
        'nombre':nombre,
        'apellido':apellido,
        'direccion':direccion,
        'state':state,
        'tel':tel,
        'grade':{
            'inicial': 0
        }
        
    }
    campers.update({id:camper})

def addTrainer(trainers:dict):
    try:
        hours = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        name = input('Ingrese en nombre compelto: ')
        id = input('Ingrese el ID: ')
        hour = input('Ingrese el rango de horas en formato de 24H ejem:(9-17) ')
        hoursMtx = list(map(int, hour.split('-')))
        print(hoursMtx)
        x = 6
        for i in range(17):
            if hoursMtx[0] <= x <= hoursMtx[1]:
                hours[i] = 1
            x += 1
        trainer = {
            'name':name,
            'id':id,
            'hours':hours
        }
        trainers.update({name.split()[0].capitalize():trainer})
    except ValueError:  # Handle non-numeric values
        print("El numero no es valido")
        addTrainer(trainers)

def assignGrade(campers:dict):
    try:
        id = input('Id del estudiante ')
        if id not in campers['campers']:
            print('El id no existe')
            assignGrade(campers)
        for key, value in campers['campers'][id]['grade'].items():
            print(key)
        module = input('Nombre del modulo a editar o nuevo modulo (escribir nuevo)')
        if module == 'nuevo':
            module = input('Nombre del modulo para asignar notas ')
            score = calcGrade()
            grade = {
                module:score
            }
            if score >= 60:
                campers['campers'][id]['state'] = 'En espera'
        else:
            score = calcGrade()
            grade = {
                module:score
            }
            if score < 60:
                if campers['campers'][id]['state'] == 'Riesgo':
                    campers['campers'][id]['state'] = 'Perdida'
                else:
                    campers['campers'][id]['state'] = 'Riesgo'
            if score >= 60:
                campers['campers'][id]['state'] = 'En curso'
        campers['campers'][id]['grade'].update(grade)
    except ValueError:
        print("El numero no es valido")
        assignGrade(campers)

def calcGrade():
    quiz = 0
    theory = float(input('Nota teorica (30%) '))
    practice = float(input('Nota practica (60%) '))
    nQuiz = int(input('Numero de quices (10%) '))
    for i in range(nQuiz):
        quiz += float(input(f'Nota Quiz {i+1} '))
    quiz = quiz / nQuiz
    return((theory*0.3)+(practice*0.6)+(quiz*0.1))

def assignStunt(campers:dict, regist:dict):
    try:
        id = input('Id del estudiante ')
        if id not in campers['campers']:
            print('El id no existe')
            assignStunt(campers)
        if campers['campers'][id]['state'] == 'Inscrito':
            print('El estudiante no ha presentado la prueba inicial ')
        else:
            for key, value in regist.items():
                print(key)
            route = input('Elija la ruta para asignar al estudiante ')
            if route not in regist:
                print('La ruta no existe')
                assignStunt(campers)
            else:
                regist[route]['students'].append(id)
                campers['campers'][id]['state'] = 'En Curso'
    except ValueError: 
        print("El numero no es valido")
        assignGrade(campers)

def generateRoute(campers: dict, regist: dict):
    global y
    try:
        route = {}
        modules = {}
        hold = {}
        schedule = [0] * 17
        name = input('Nombre del trainer: ')
        if name.capitalize() not in campers['trainers']:
            print('El trainer no existe')
            return generateRoute(campers, regist) 
        route.update({"trainer": name})
        modules.update({'introduccion':campers['modules']['intro']})
        modules.update({'web':campers['modules']['web']})
        for i in ['formal', 'data', 'back']:
            for key, value in campers['modules'][i].items(): 
                print(value)
            mod = input(f'Ingrese los temas para el modulo {i} (si ingresa más, sepárelos por comas): ')
            modul = mod.split(',')
            for topic in modul:
                hold.update({topic.strip().lower(): topic.strip().capitalize()})
            modules.update({i: hold})
            hold = {}
        route.update({'modules': modules})
        route.update({'students': []})
        hour = input('Ingrese el rango de horas de clase en formato de 24H ejem:(10-14): ')
        hoursMtx = list(map(int, hour.split('-')))
        if checkSchedule(campers['trainers'][name.split()[0].capitalize()]['hours'], hoursMtx[0], hoursMtx[1]):
            x = 6
            for i in range(17):
                if hoursMtx[0] <= x <= hoursMtx[1]:
                    campers['trainers'][name.split()[0].capitalize()]['hours'][i] += 1
                x += 1
            
        else:
            print('El horario no es viable para el trainer')
            return generateRoute(campers, regist) 
        x = 6
        for i in range(17):
            if hoursMtx[0] <= x <= hoursMtx[1]:
                schedule[i] = 1
            x += 1
        route.update({'schedule': schedule})
        for i in ['apolo', 'artemis', 'sputnik']:
            print(i)
        zone = input('Ingrese la zona para dar las clases: ')
        if zone not in ['apolo', 'artemis', 'sputnik']:
            print('El salon no existe')
            return generateRoute(campers, regist) 
        route.update({'zone': zone})
        route.update({'start': input('Fecha de inicio: ')})
        route.update({'end': input('Fecha de finalizacion: ')})
        identify = [name.split()[0].capitalize()[0],y]
        identy = identify[0] + str(identify[1])
        y += 1
        return {identy:route} 
    except Exception as e:  
        print(f"An error occurred: {e}")
        return {} 


def checkSchedule(trainerSchedule, startHour, endHour):
    valid_hours = range(6, 23)
    if startHour not in valid_hours or endHour not in valid_hours:
        return False
    if endHour <= startHour:
        return False
    for hour in range(startHour, endHour):
        if trainerSchedule[hour - 6] == 1:
            pass
    return True

def inscrit(campers: dict, regist: dict):
    x = 0
    for key, value in campers['campers'].items():
        if campers['campers'][key]['state'] == 'Inscrito':
            print(key)
            x += 1
    print(f'Estos son los {x} campers inscritos')

def espera(campers: dict, regist: dict):
    x = 0
    for key, value in campers['campers'].items():
        if campers['campers'][key]['state'] == 'En espera':
            print(key)
            x += 1
    print(f'Estos son los {x} campers en espera de ser asignados a un curso')

def trains(campers: dict, regist: dict):
    x = 0
    for key, value in campers['trainers'].items():
        print(campers['trainers'][key]['name'])
        x += 1
    print(f'Estos son los {x} trainers')

def bajo(campers: dict, regist: dict):
    x = 0
    for key, value in campers['campers'].items():
        if campers['campers'][key]['state'] == 'Riesgo':
            print(key)
            x += 1
    print(f'Estos son los {x} campers con bajo rendimiento')

def trainscamps(campers: dict, regist: dict):
    for key, value in regist.items():
        print(regist[key]['trainer'])
        for i in regist[key]['students']:
            print(i)

def aprove(campers: dict, regist: dict):
    for key, value in regist.items():
        print(f'Clase {key}')
        for i in regist[key]['students']:
            if campers['campers'][i]['state'] == 'perdida':
                no = campers['campers'][i]['nombre']
                print(f'El camper {no} no aprobo')
            elif campers['campers'][i]['state'] == 'En curso':
                si = campers['campers'][i]['nombre']
                print(f'El camper {si} esta en curso')
