from django.test import TestCase
from .models import Pais, Provincia, Localidad

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

class EncargadoTestCase(TestCase):
    fixtures = FIXTURES
    def setUp(self):
        pass

    def test_crear_encargado(self):
        pass

class VendedorTestCase(TestCase):
    fixtures = FIXTURES
    def setUp(self):
        pass

    def test_crear_encargado(self):
        pass

class ClienteTestCase(TestCase):
    fixtures = FIXTURES
    def setUp(self):
        pass

    def test_crear_encargado(self):
        pass