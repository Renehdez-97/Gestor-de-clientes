import os
import helpers
import database as db

def iniciar():
    while True:
        helpers.limpiar_pantalla()

        print("===== ===== ===== ==== ==== ====")
        print("===== BIENVENIDO AL GESTOR =====")
        print("===== ===== ===== ==== ==== ====")
        print("[1] Listar a los clientes")
        print("[2] Buscar un cliente    ")
        print("[3] Añadir un cliente    ")
        print("[4] Modificar un cliente ")
        print("[5] Borrar un cliente    ")
        print("[6] Cerrar el Gestor     ")

        opcion = input('> ') 
        helpers.limpiar_pantalla()

        if opcion == '1':
            print('Obteniendo desde la base de datos el listado de los Clientes...\n')
            for cliente in db.Clientes.lista:
                print(cliente)
            

        elif opcion == '2':
            print('Un momento, Buscando un cliente...\n')
            dni = helpers.leer_texto(4, 4, 'DNI (1 char y 3 int)').upper()
            cliente = db.Clientes.buscar(dni)
            print(cliente) if cliente else print('No se a encontrado el cliente.')

        elif opcion == '3':
            print('Listo, puedes añadir un cliente...\n')

            dni = None
            while True:
                dni = helpers.leer_texto(4, 4, 'DNI (1 char y 3 int)').upper()
                if helpers.validar_dni(dni, db.Clientes.lista):
                    break

            nombre = helpers.leer_texto(3, 30, 'Nombre (de 2 a 30 chars)').capitalize()
            apellido = helpers.leer_texto(3, 30, 'Apellido (de 2 a 30 chars)').capitalize()
            db.Clientes.crear(dni, nombre, apellido)
            print('Se a añadido correctamente el cliente')

        elif opcion == '4':
            print('Modificando un cliente...\n')
            dni = helpers.leer_texto(4, 4, 'DNI (1 char y 3 int)').upper() #primero buscamos el dni del cliente que queremos buscar
            cliente = db.Clientes.buscar(dni) #aqui buscamos el cliente, para saber si existe
            if cliente: #si existe el cliente
                nombre = helpers.leer_texto(3, 30, f'Nombre (de 2 a 30 chars)[{cliente.nombre}]').capitalize() #leemos el nombre y apellido que queremos modificar
                apellido = helpers.leer_texto(3, 30, f'Apellido (de 2 a 30 chars) [{cliente.apellido}]').capitalize()
                db.Clientes.modificar(cliente.dni, nombre, apellido) #ponemos cliente.dni ya que ese no se puede modificar
                print('Se a modificado correctamente el cliente')
            else:
                print('No se a encontrado el cliente')



        elif opcion == '5':
            print('Se está borrando un cliente...\n')
            dni = helpers.leer_texto(4, 4, 'DNI (1 char y 3 int)').upper()
            print("Se a borrado el cliente correctamente.") if db.Clientes.borrar(dni) else print("No se encontró el cliente.")

        elif opcion == '6':
            print('Saliendo del sistema...\n')
            break

        input("\nPresiona ENTER para continuar...")
