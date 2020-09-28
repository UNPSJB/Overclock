from django.test import TestCase
from .models import Pais, Provincia, Localidad

class ZonaTestCase(TestCase):
    fixtures = ['./core/fixtures/base.json']
    def setUp(self):
        pass

    def test_crear_zona(self):
        pass

class EncargadoTestCase(TestCase):
    fixtures = ['./core/fixtures/base.json']
    def setUp(self):
        pass

    def test_crear_encargado(self):
        pass

class VendedorTestCase(TestCase):
    fixtures = ['./core/fixtures/base.json']
    def setUp(self):
        pass

    def test_crear_encargado(self):
        pass

class ClienteTestCase(TestCase):
    fixtures = ['./core/fixtures/base.json']
    def setUp(self):
        pass

    def test_crear_encargado(self):
        pass