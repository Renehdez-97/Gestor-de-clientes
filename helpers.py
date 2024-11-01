import os
import platform
import re


def limpiar_pantalla():
    os.system('cls') if platform.system()=="Windows" else os.system('clear')

def leer_texto(longitud_min=0, longitud_max=100, mensaje=None):
    print(mensaje) if mensaje else None
    while True:
        texto = input('> ')
        if len(texto) >= longitud_min and len(texto) <= longitud_max:
            return texto
        
def validar_dni(dni, lista):
    if not re.match('[A-Z][0-9]{3}$', dni): #Si no concuerda que? 1.una letra mayuscula, que acontinuacion un numero del 0-9 comprendido por 3 digitos, termino con un $
        print('DNI incorrecto, ingrese el orden debido')
        return False
    for cliente in lista:
        if cliente.dni == dni:
            print('este DNI ya a sido utilizado')
            return False
    return True