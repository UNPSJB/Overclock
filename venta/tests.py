from django.test import TestCase
from core.models import Cliente, Vendedor
from hotel.models import Hotel 
from datetime import datetime
from .models import Factura, Liquidacion 

FIXTURES = [
    './core/fixtures/auth.json',
    './core/fixtures/base.json',
    './hotel/fixtures/base.json',
    #'./venta/fixtures/base.json'
    ]

class FacturaTestCase(TestCase):
    fixtures = FIXTURES
    def setUp(self):
        self.hotel = Hotel.objects.first() 
        self.cliente = Cliente.objects.first() 
        self.vendedor = Vendedor.objects.first() 

    def test_alquilar(self):
        self.factura = Factura.objects.create(cliente=self.cliente, vendedor=self.vendedor)
        habitacion = self.hotel.habitaciones.first()
        habitaciones = [habitacion]
        # 5 noches en temporada alta = 1800, sin descuento
        alquiler = self.factura.alquilar_habitaciones_de_hotel(self.hotel, 
            habitaciones, 
            10, 
            datetime(2021, 1, 1), 
            datetime(2021, 1, 6))
        self.assertEqual(alquiler.total, 5 * 1800)
