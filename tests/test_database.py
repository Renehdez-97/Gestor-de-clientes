import unittest
import database as db
import copy
import helpers

class TestDatabase (unittest.TestCase):
    def setUp(self):
        db.Clientes.lista= [
            db.Cliente('A001', 'Balto', 'Hernandez'),
            db.Cliente('B002', 'Nike', 'Aguirre'),
            db.Cliente('C003', 'Lia', 'Aguirre')
        ]

    def test_buscar_cliente(self):
        cliente_existente = db.Clientes.buscar('A001')
        cliente_inexistente = db.Clientes.buscar('Z999')
        self.assertIsNotNone (cliente_existente)
        self.assertIsNone (cliente_inexistente)

    def test_crear_cliente (self):
        nuevo_cliente = db.Clientes.crear('D004', 'Bety', 'La_Fea')
        self.assertEqual (len(db.Clientes.lista),4)
        self.assertEqual(nuevo_cliente.dni, 'D004')
        self.assertEqual(nuevo_cliente.nombre, 'Bety')
        self.assertEqual(nuevo_cliente.apellido, 'La_Fea')

    def test_modificar_cliente (self):
        cliente_a_modificar = copy.copy(db.Clientes.buscar ('C003'))
        cliente_modificado = db.Clientes.modificar('C003','Lia', 'La_Gorda')
        self.assertEqual(cliente_a_modificar.apellido, 'Aguirre' )
        self.assertEqual( cliente_modificado.apellido, 'La_Gorda')

    def test_borrar_cliente (self):
        cliente_borrado = db.Clientes.borrar ('B002')
        cliente_volviendo_a_buscar = db.Clientes.buscar('B002')
        self.assertEqual(cliente_borrado.dni, 'B002')
        self.assertIsNone(cliente_volviendo_a_buscar)

    def test_validar_dni (self):
        #comprobamos si se vuelve verdadero
        self.assertTrue(helpers.validar_dni('F123', db.Clientes.lista))
        self.assertFalse(helpers.validar_dni('df0123', db.Clientes.lista))
        self.assertFalse(helpers.validar_dni('123F', db.Clientes.lista))
        self.assertFalse(helpers.validar_dni('C003', db.Clientes.lista)) #UN CLIENTE QUE YA EXISTE