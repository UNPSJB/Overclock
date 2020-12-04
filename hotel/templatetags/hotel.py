from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def hotel_disponible(context, hotel):
    inicio = context.get('fecha_inicio', None)
    fin = context.get('fecha_fin', None)
    pasajeros = context.get('pasajeros', None)
    if pasajeros is not None:
        print("Hola")
        print(pasajeros)
        return hotel.disponible(inicio, fin, pasajeros)
    else:
        return True 