$(function () {
    $('#table_historial_riegos').DataTable({
        responsive: true, //se adapta la tabla
        autoWidth: false, //respeta el ancho de mi tabla
        destroy: true, //se puede reinicializar con otro proceso
        deferRender: true, //
        ajax: {
            url: window.location.pathname, //
            type: 'POST',
            data: {
                'action': 'load_historial_riegos'
            }, //parametros
            dataSrc: "" //tengo datos con una variable
        },
        columns: [ //columnas de las tablas, se debe poner los campos del models.py
            {"data": "id"},
            {"data": "codigo_sensor"},
            {"data": "fecha_riego"},
            {"data": "tiempo_riego"},
            {"data": "valor_humed_suelo"},
            {"data": "valor_humed_ambiente"},
            {"data": "valor_temp_ambiente"},
            {"data": "valor_evapotranspiracion"},
            {"data": "device"},
            {"data": "persona"},
            {"data": "tipo_logica_difusa"},
            {"data": "tipo_rol"},
        ],
        order: [[0, 'desc']],
        dom: 'Bfrtip', //esto me permite eliminar el combobox de numero de registros para reemplazar con los buttons
        buttons: [
            'copyHtml5',
            'excelHtml5',
            'csvHtml5',
            'pdfHtml5',
            'print'
        ],
        initComplete: function (settings, json) {
            //aqui va alguna funcion que se ejecutara despues de cargar la tabla
        }

    });
})