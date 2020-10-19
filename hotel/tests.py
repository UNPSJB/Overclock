from django.test import TestCase
from .models import Hotel, Habitacion 

class HotelesTestCase(TestCase):
    fixtures = [
      './core/fixtures/base.json',
      './hotel/fixtures/base.json'
      ]
    def setUp(self):
        pass

    def test_buscar_en_zona(self):
        pass
