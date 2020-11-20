/*script para abrir modales recibe por parametros la url y el id*/

    function abrir_modal(url, id) { /// al llamar a la funcion para apertura de modales le damos url del modal y id del mismo
        $(id).load(url, function () {
            //$(this).modal('show');
        });
    }
