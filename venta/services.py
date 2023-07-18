from datetime import datetime
from core.models import Vendedor
from venta.models import Factura, Liquidacion
from venta.helpers import cliente_existe

def buscar_monto_total_liquidaciones_pendientes(fecha_inicio, fecha_fin, vendedor):
    facturas = Factura.objects.filter(
        liquidacion__isnull=True,
        vendedor=vendedor,
        fecha__range=(fecha_inicio, fecha_fin)
    )
    total = sum([f.total() for f in facturas]) * vendedor.coeficiente
    return total

def cargar_liquidaciones_pendientes(fecha_inicio, fecha_fin):
    vendedores = Vendedor.objects.all()
    facturas_pendientes = []
    for vendedor in vendedores:
        monto_total_pendiente = buscar_monto_total_liquidaciones_pendientes(fecha_inicio, fecha_fin, vendedor)
        if monto_total_pendiente != 0:
            persona_dict = {
                    'nombre': vendedor.persona.nombre,
                    'apellido': vendedor.persona.apellido,
                    'monto_total': monto_total_pendiente,
                }
            facturas_pendientes.append(persona_dict)
    return facturas_pendientes

def buscar_facturas_pendiente_de_liquidar(fecha_inicio, fecha_fin, vendedor):
    facturas = Factura.objects.filter(
        liquidacion__isnull=True,
        vendedor=vendedor,
        fecha__range=(fecha_inicio, fecha_fin)
    )
    return facturas

def liquidar_liquidaciones_pendientes(fecha_inicio, fecha_fin):
    vendedores = Vendedor.objects.all()
    for vendedor in vendedores:
      facturas_pendiente_de_liquidar = buscar_facturas_pendiente_de_liquidar(fecha_inicio, fecha_fin, vendedor)
      if len(facturas_pendiente_de_liquidar) > 0:
        monto_total = buscar_monto_total_liquidaciones_pendientes(fecha_inicio, fecha_fin, vendedor)
        liquidacion = Liquidacion(abonado=datetime.now(), vendedor=vendedor, total=monto_total)
        liquidacion.save()
        for factura_pendiente_de_liquidar in facturas_pendiente_de_liquidar:
            factura_pendiente_de_liquidar.liquidacion = liquidacion
            factura_pendiente_de_liquidar.save()
            

def documento_valido(dni_nuevo , form):
    if not dni_nuevo.isnumeric():
        form.add_error('documento', 'ingrese un documento valido')
        return False
    if cliente_existe(dni_nuevo):
        form.add_error('documento', 'DNI ya existe en el sistema')
        return False
    return True
        
