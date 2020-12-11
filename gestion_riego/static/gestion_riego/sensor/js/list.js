$(function() {
    $('#data').DataTable({
        responsive: true, //se adapta la tabla
        autoWidth: false, //respeta el ancho de mi tabla
        destroy: true, //se puede reinicializar con otro proceso
        deferRender: true, //
        ajax: {
            url: window.location.pathname, //
            type: 'POST',
            data: {
                'action': 'searchdata'
            }, //parametros
            dataSrc: "" //tengo datos con una variable
        },
        columns: [ //columnas de las tablas, se debe poner los campos del models.py
            {"data": "id"},
            {"data": "codigo_sensor"},
            {"data": "tipo_sensor.nombre"},
            {"data": "fecha_registro"},
            {"data": "value"},
            {"data": "estado"},
            {"data": "device.nombre"},
            {"data": "Opciones"},
        ],
        columnDefs: [ //Por columna lo puedes personalizar
            {
                targets: [-1], //voy de atras hacia arriba
                class: 'text-center',
                orderable: false,
                render: function(data, type, row) {
                    //buttons: me creo mis botones con html, recuerda que estoy accediendo mediante objetos
                    var buttons = '<a href="/gestion_riego/sensor_update/'+row.id+'/" class="btn btn-secondary"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/gestion_riego/sensor_delete/'+row.id+'/" class="btn btn-secondary"><i class="fas fa-trash-alt"></i></a>'
                    return buttons;
                }
            },

        ],
        order: [[0, 'desc']],
        buttons: [
            'copyHtml5',
            'excelHtml5',
            'csvHtml5',
            'pdfHtml5',
            'print'
        ],
        initComplete: function(settings, json){
            //aqui va alguna funcion que se ejecutara despues de cargar la tabla
        }
    });
});
