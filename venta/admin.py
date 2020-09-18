from django.contrib import admin

from django.contrib import admin
from .models import (Liquidacion, Factura, Alquiler)

for model in [Liquidacion, Factura, Alquiler]:
    admin.site.register(model)
