from django import template
from core.models import TipoHabitacion

from hotel.models import PrecioPorTipo, TemporadaAlta

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
    
 
def devolver_temporadas_en_fechas(temporadas, fecha_inicio, fecha_fin):
    temporadas_en_rango=[]
    for temporada in temporadas:
        if (( fecha_inicio <= temporada.inicio <= fecha_fin) or (fecha_inicio <= temporada.fin <= fecha_fin)):
            temporadas_en_rango.append(temporada)
    return temporadas_en_rango
    


@register.simple_tag(takes_context=True)
def asignar_precio_por_temporada(fecha_inicio, fecha_fin, id_hotel, tipo_habitacion):
    temporadas = TemporadaAlta.objects.filter(hotel = id_hotel)
    precio_Hotel_temporadas = PrecioPorTipo.objects.get( hotel_id = id_hotel, tipo_id = tipo_habitacion)
    print(precio_Hotel_temporadas)
    dias_promocion = 0
    dias_sin_promocion = 0
    total = 0
    resultado = 0
    if (temporadas):
        temporadas = devolver_temporadas_en_fechas(temporadas, fecha_inicio, fecha_fin)
        print(temporadas)
        for temporada in temporadas:
            if (fecha_inicio <= fecha_fin <= temporada.inicio) or (temporada.fin <= fecha_inicio <= fecha_fin):
                dias_sin_promocion = fecha_fin - fecha_inicio
                dias_sin_promocion = dias_sin_promocion.days * precio_Hotel_temporadas.baja
                total =  dias_sin_promocion
            
            if((fecha_inicio < temporada.inicio) and (temporada.inicio <= fecha_fin <= temporada.fin)):
                dias_promocion = fecha_fin - temporada.inicio
                dias_promocion = dias_promocion.days * precio_Hotel_temporadas.alta
                dias_sin_promocion = temporada.inicio - fecha_inicio
                dias_sin_promocion = dias_sin_promocion.days * precio_Hotel_temporadas.baja
                total = dias_promocion + dias_sin_promocion
            
            if((temporada.inicio <= fecha_inicio <= temporada.fin) and (temporada.fin <= fecha_fin)):
                dias_promocion = temporada.fin - fecha_inicio
                dias_promocion = dias_promocion.days * precio_Hotel_temporadas.alta
                dias_sin_promocion = fecha_fin - temporada.fin
                dias_sin_promocion = dias_sin_promocion.days * precio_Hotel_temporadas.baja
                total = dias_promocion + dias_sin_promocion
            
            if (temporada.inicio <= fecha_inicio) and (temporada.fin >= fecha_fin):
                dias_promocion = fecha_fin - fecha_inicio
                dias_promocion = dias_promocion.days * precio_Hotel_temporadas.alta
                total = dias_promocion
            
            if ((fecha_inicio <= temporada.inicio <= temporada.fin) and (temporada.fin <= fecha_fin)):
                dias_sin_promocion = (fecha_fin - temporada.fin ) + ( temporada.inicio - fecha_inicio)
                dias_sin_promocion = dias_sin_promocion.days * precio_Hotel_temporadas.baja
                dias_promocion = temporada.fin - temporada.inicio
                dias_promocion = dias_promocion.days * precio_Hotel_temporadas.alta
                total =  dias_promocion + dias_sin_promocion
            print (dias_sin_promocion)
            print(dias_promocion)
            resultado = resultado + total
            fecha_inicio = temporada.fin
        return resultado
    else:   
        return (fecha_fin - fecha_inicio).days * precio_Hotel_temporadas.baja           
                
    

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
