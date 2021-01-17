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
            {"data": "tiempo_riego_1_variable"},
            {"data": "tiempo_riego_4_variable"},
            {"data": "valor_humed_suelo"},
            {"data": "valor_humed_ambiente"},
            {"data": "valor_temp_ambiente"},
            {"data": "valor_evapotranspiracion"},
            {"data": "device"},
            {"data": "persona"},
            {"data": "tipo_logica_difusa"},
            {"data": "tipo_rol"},
            {"data": "image_1_variable"},
            {"data": "image_3_variable"},
            {"data": "image_4_variable"},

        ],
        columnDefs: [
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<img src="'+data+'" class="img-fluid d-block mx-auto" style="width: 20px; height: 20px;">';
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<img src="'+data+'" class="img-fluid d-block mx-auto" style="width: 20px; height: 20px;">';
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<img src="'+data+'" class="img-fluid d-block mx-auto" style="width: 20px; height: 20px;">';
                }
            },
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