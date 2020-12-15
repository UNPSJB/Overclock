from django.shortcuts import get_object_or_404
from hotel.models import Hotel, Habitacion, PaqueteTuristico


class Carrito:
    def __init__(self,request):
        self.request=request
        self.session=request.session
        carrito=self.session.get("carrito")
        #print(carrito)
        if carrito==None:
            print("SE CREA CARRITO!!!!!!!!")
            carrito=self.session["carrito"]={}
            self.carrito=carrito
        else:
            print("SE REUSA CARRITO!!!!!!!!")
            self.carrito=carrito
        self.save()

    def save(self):
        self.session["carrito"]=self.carrito
        self.session.modified=True
           
#*************************GESTION HABITACION DE CARRITO **************************************
    def agregar_habitacion(self,habitacion,desde,hasta,pasajeros):
        claves=list(self.carrito.keys())
        if str(habitacion) not in claves:
            print("entre a crear un alquiler nuevo de otra habitacion")
            self.carrito[habitacion]={
                "alquiler":[]                
                }
            self.carrito[habitacion]["alquiler"].append([str(desde),str(hasta),str(pasajeros)])
            
        else:
            print("reuso la habitacion")
            periodoDisponible=True
            alquileres = list(self.carrito[str(habitacion)]["alquiler"])
            for index in alquileres:
                print(index)
                desde_contenido = (str(desde)>=index[0] and str(desde)<=index[1])
                hasta_contenido = (str(hasta)>=index[0] and str(hasta)<=index[1])
                esta_contenido = (str(desde)<=index[0] and str(hasta)>=index[1])
                print(desde_contenido," ",hasta_contenido," ",esta_contenido)
                if (desde_contenido or hasta_contenido or esta_contenido):
                    print("no puedo alquilar")
                    periodoDisponible=False
                    break
            if periodoDisponible:
                self.carrito[str(habitacion)]["alquiler"].append([str(desde),str(hasta),str(pasajeros)])
        self.save()

   
    
    def quitar_habitacion(self, habitacion, desde, hasta):
        claves=list(self.carrito.keys())
        if str(habitacion) in claves:
            if len(self.carrito[str(habitacion)]["alquiler"])==1:
                print("borro Habitacion")
                del self.carrito[str(habitacion)]
            else:
                print("busco alquiler")
                alquileres = list(self.carrito[str(habitacion)]["alquiler"])
                for index in alquileres:
                    if str(desde) and str(hasta) in index:
                        print("borro lo que encontre")
                        self.carrito[str(habitacion)]["alquiler"].remove(index)
        self.save()

#*************************GESTION PAQUETE DE CARRITO **************************************

    def agregar_paquete(self,paquete,pasajeros):
        paqueteInstancia=get_object_or_404(PaqueteTuristico,pk=paquete)
        clave_instancia="p"+str(paqueteInstancia.pk)
        claves=list(self.carrito.keys())
        if clave_instancia not in claves:
            print("entre a crear un alquiler nuevo de otro paquete")
            self.carrito[clave_instancia]={
                "paquete_pk":str(paqueteInstancia.pk),
                "nombre":paqueteInstancia.nombre,
                "pasajeros":str(pasajeros)                
                }
        else:
            print("imposible agregar")
        self.save()

    
    def quitar_paquete(self, paquete):
        clave_instancia="p"+str(paquete)
        claves=list(self.carrito.keys())
        if clave_instancia in claves:
            del self.carrito[clave_instancia]
        else:
            print("no esta el paquete en el carrito")
        self.save()



    def get_alquileres_paquetes(self): 
        col_paquetes=[]
        for key,value in self.carrito.items():
            if "p" in key:
                paquete_pk=int(value["paquete_pk"])
                paqueteInstancia=get_object_or_404(PaqueteTuristico,pk=paquete_pk)
                col_paquetes.append(paqueteInstancia)
        return col_paquetes


    def get_alquileres_habitaciones(self):
        col_habitaciones=[]
        for key in self.carrito.items():
            if "p" not in str(key):
                habitacionInstancia=get_object_or_404(Habitacion,pk=key)
                col_habitaciones.append(habitacionInstancia)
        return col_habitaciones

# Hacer 3 metodos get_alquileres, get_alquileres_habitaciones, get_alquileres_paquetes
# metodo para crear Factura -> Alquileres carrito.facturar()