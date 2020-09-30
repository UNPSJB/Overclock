from django.test import TestCase
from decimal import Decimal
from .models import (Pais, Provincia, Localidad, 
    Persona, Encargado, Vendedor, Cliente)

FIXTURES = [
    './core/fixtures/auth.json',
    './core/fixtures/base.json'
    ]

class ZonaTestCase(TestCase):
    fixtures = FIXTURES
    def setUp(self):
        pass

    def test_crear_zona(self):
        pass

class ServicioTestCase(TestCase):
    fixtures = FIXTURES
    def setUp(self):
        self.trelew = Localidad.objects.filter(nombre="Trelew").first()

    def test_crear_zona(self):
        zona = Localidad.objects.crear_zona("Trelew")
        self.assertTrue(self.trelew in zona)
        zona = Localidad.objects.crear_zona("Chubut")
        self.assertTrue(self.trelew in zona)
        zona = Localidad.objects.crear_zona("Argentina")
        self.assertTrue(self.trelew in zona)

class CategoriaTestCase(TestCase):
    fixtures = FIXTURES
    def setUp(self):
        pass

    def test_crear_zona(self):
        pass

class PersonaTestCase(TestCase):
    fixtures = FIXTURES
    def setUp(self):
        self.persona = Persona.objects.create(
            nombre="Pepe", 
            tipo_documento=Persona.DNI,
            documento="23423435")
    
class EncargadoTestCase(PersonaTestCase):
    def test_promover_encargado(self):
        self.persona.agregar_rol(Encargado())
        self.assertTrue(self.persona.sos(Encargado))
        #self.assertFalse(self.persona.como(Encargado).clave == "")

class VendedorTestCase(PersonaTestCase):
    def test_promover_vendedor(self):
        self.persona.agregar_rol(Vendedor())
        self.assertTrue(self.persona.sos(Vendedor))
        #self.assertTrue(self.persona.como(Vendedor).coeficiente == Decimal(0))
        #self.assertNotNone(self.persona.usuario)
        #self.assertTrue(self.persona.usuario.has_perm('core.add_cliente'))
        #self.assertFalse(self.persona.usuario.has_perm('core.add_servicio'))

class ClienteTestCase(PersonaTestCase):
    def test_promover_cliente(self):
        self.persona.agregar_rol(Cliente())
        self.assertTrue(self.persona.sos(Cliente))
        #self.assertTrue(self.persona.como(Cliente).puntos == 0)