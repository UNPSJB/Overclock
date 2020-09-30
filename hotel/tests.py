from django.test import TestCase
from .models import Hotel, Habitacion 

FIXTURES = [
    './core/fixtures/auth.json',
    './core/fixtures/base.json',
    './hotel/fixtures/base.json'
    ]

class HotelesTestCase(TestCase):
    fixtures = FIXTURES
    def setUp(self):
        pass

    def test_buscar_en_zona(self):
        pass
