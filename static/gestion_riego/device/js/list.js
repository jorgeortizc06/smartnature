$(function () {
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
        columns: [ //columnas de las tablas
            {"data": "id"},
            {"data": "nombre"},
            {"data": "descripcion"},
            {"data": "ip"},
            {"data": "topic"},
            {"data": "puerto"},
            {"data": "frecuencia_actualizacion"},
            {"data": "tipo_logica_difusa"},
            {"data": null},
        ],
        columnDefs: [ //Por columna lo puedes personalizar
            {
                targets: [-1], //voy de atras hacia arriba
                class: 'text-center',
                orderable: false,
                render: function(data, type, row) {
                    //buttons: me creo mis botones con html, recuerda que estoy accediendo mediante objetos
                    var buttons = '<a href="/gestion-riego/devices/update/' + row.id + '/" class="btn btn-secondary btnEdit"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/gestion-riego/devices/delete/' + row.id + '/" rel="btnDelete" class="btn btn-secondary"><i class="fas fa-trash-alt"></i></a>'
                    return buttons;
                }
            },
        ],
        order: [[0, 'desc']], //ordeno la primera columna descendente
        initComplete: function(settings, json){
            //aqui va alguna funcion que se ejecutara despues de cargar la tabla
        }
    });
})

