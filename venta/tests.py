from django.test import TestCase
from .models import Factura, Liquidacion 

class HotelesTestCase(TestCase):
    fixtures = [
      './core/fixtures/base.json',
      './hotel/fixtures/base.json',
      './venta/fixtures/base.json'
      ]
    def setUp(self):
        pass

    def test_(self):
        pass
