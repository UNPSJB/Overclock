from hotel.models import Habitacion

def habitacion_duplicada(nueva_habitacion , hotel_id , form):
    habitaciones = Habitacion.objects.filter(hotel = hotel_id)
    for habitacion in habitaciones:
        if int(habitacion.numero) == int(nueva_habitacion) :
            form.add_error('numero', 'el numero de habitacion ya existe en este hotel')
            return True
            break
    return False