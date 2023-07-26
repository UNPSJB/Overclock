from django import template

from venta.services import asignar_precio_por_temporada

register = template.Library()


@register.simple_tag(takes_context=True)
def hotel_disponible(context, hotel):
    inicio = context.get('fecha_inicio', None)
    fin = context.get('fecha_fin', None)
    pasajeros = context.get('pasajeros', None)
    if pasajeros is not None:
        print(pasajeros)
        print(inicio, fin)
        print(hotel.disponible(inicio, fin, pasajeros))
        return hotel.disponible(inicio, fin, pasajeros)
    else:
        return True 
    

@register.simple_tag(takes_context=True)
def precio_entre_fechas(context, habitacion , hotel_id):
    inicio = context.get('fecha_inicio', None)
    fin = context.get('fecha_fin', None)
    if inicio is not None:
        if fin is not None:
            precio_final_por_temporada = asignar_precio_por_temporada(inicio, fin, hotel_id, habitacion.tipo_id)
            return precio_final_por_temporada
    else:
        return 0
