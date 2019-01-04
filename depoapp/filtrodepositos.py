def get_grupos(user):
	l = ""
	for g in user.groups.all():
		l = l + g.name
	return l


def permisoRw(user):
	if("Deposito-Zona Rawson" in get_grupos(user)):
		return 5
	else:
		return 0

def permisoSarmiento(user):
	if("Deposito-Zona Sarmiento" in get_grupos(user)):
		return 1
	else:
		return 0

def permisoMadryn(user):
	if("Deposito-Zona Madryn" in get_grupos(user)):
		return 2
	else:
		return 0
	
def permisoEsquel(user):
	if("Deposito-Zona Esquel" in get_grupos(user)):
		return 3
	else:
		return 0
	
def permisoGaiman(user):
	if("Deposito-Zona Gaiman" in get_grupos(user)):
		return 4
	else:
		return 0
	
def permisoJefe(user):
	if("Deposito-Zona Gaiman" in get_grupos(user)):
		return 0

def obtenerUsuario(user):
	if ("Deposito-Zona Rawson" in get_grupos(user)):
		return 5
	else:
		if("Deposito-Zona Sarmiento" in get_grupos(user)):
			return 1
		else:
			if("Deposito-Zona Madryn" in get_grupos(user)):
				return 2
			else:
				if("Deposito-Zona Esquel" in get_grupos(user)):
					return 3
				else:
					if("Deposito-Zona Gaiman" in get_grupos(user)):
						return 4
					else:
						if("Deposito-Zona Trevelin" in get_grupos(user)):
							return 6
						else:
							if("Deposito-Jefe-Depositos" in get_grupos(user)):
								return 0
							else:
								return 0