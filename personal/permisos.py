# -*- coding: utf-8 -*-

def get_grupos(user):
    l = ""
    for g in user.groups.all():
        l = l + g.name
    return l


def permisoListado(user):
    if("Personal-Listados" in get_grupos(user))  or ((user.username) == 'admin'):
        return False
    else:
        return True

def permisoEstadistica(user):
    if("Estadisticas" in get_grupos(user))  or ((user.username) == 'admin'):
        return False
    else:
        return True

def permisoZona(user):
    if("Zona" in get_grupos(user))  or ((user.username) == 'admin'):
        return False
    else:
        return True
	
	
def permisoABM(user):
    if("ABM" in get_grupos(user))  or ((user.username) == 'admin'):
        return False
    else:
        return True

def permisoDatosAgente(user):
    if("Datos Agente" in get_grupos(user))  or ((user.username) == 'admin'):
        return False
    else:
        return True	
	
def permisoAusent(user):
    if("Ausent" in get_grupos(user))  or ((user.username) == 'admin'):
        return False
    else:
        return True


def permisoCambios(user):
    if("Cambios" in get_grupos(user))  or ((user.username) == 'admin'):
        return False
    else:
        return True


def permisoEliminar(user):
    if("Eliminar" in get_grupos(user))  or ((user.username) == 'admin'):
        return False
    else:
        return True

def permisoAgente(user):
    if ((user.username) == 'admin'):
        return 'admin'
    elif ("Personal - J.CENTRO" in get_grupos(user)):
        return 'Centro'
    elif ("Personal - J.CENTRAL" in get_grupos(user)):
        return 'Central'
    elif ("Personal - J.NORESTE" in get_grupos(user)):
        return 'NorEste'
    elif ("Personal - J.NOROESTE" in get_grupos(user)):
        return 'NorOeste'
    elif ("Personal - J.NOROESTE-Puentes" in get_grupos(user)):
        return 'NorOeste-Subd Puentes'
    elif ("Personal - J.SUR" in get_grupos(user)):
        return 'Sur'
    elif ("Personal - J.SUR-Comorodo" in get_grupos(user)):
        return 'Sur - Comodoro Rivadavia'
    elif ("Personal - J.TREVELIN" in get_grupos(user)):
        return 'Trevelin'
	