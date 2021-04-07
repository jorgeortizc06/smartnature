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
            {"data": "tiempo_riego_1_variable"},
            {"data": "image_1_variable"},
            {"data": "tiempo_riego"},
            {"data": "image_3_variable"},
            {"data": "tiempo_riego_4_variable"},
            {"data": "image_4_variable"},
            {"data": "valor_humed_suelo"},
            {"data": "valor_humed_ambiente"},
            {"data": "valor_temp_ambiente"},
            {"data": "valor_evapotranspiracion"},
            {"data": "device"},
            //{"data": "persona"},
            //{"data": "tipo_logica_difusa"},
            //{"data": "tipo_rol"},
        ],
        columnDefs: [
            {
                targets: [4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<img src="'+data+'" class="img-fluid d-block mx-auto" style="width: 320px; height: 240px;">';
                }
            },
            {
                targets: [6],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<img src="'+data+'" class="img-fluid d-block mx-auto" style="width: 320px; height: 240px;">';
                }
            },
            {
                targets: [8],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<img src="'+data+'" class="img-fluid d-block mx-auto" style="width: 320px; height: 240px;">';
                }
            },
        ],
        order: [[0, 'desc']],
        initComplete: function (settings, json) {
            //aqui va alguna funcion que se ejecutara despues de cargar la tabla
        }

    });
})