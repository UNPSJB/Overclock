from django.test import TestCase
from .models import Factura, Liquidacion 

FIXTURES = [
    './core/fixtures/auth.json',
    './core/fixtures/base.json',
    './hotel/fixtures/base.json',
    #'./venta/fixtures/base.json'
    ]

class HotelesTestCase(TestCase):
    fixtures = FIXTURES
    def setUp(self):
        pass

    def test_(self):
        pass
