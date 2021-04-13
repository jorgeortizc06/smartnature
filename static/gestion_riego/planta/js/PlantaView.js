function loadPlantas() {
    $('#table_plantas').DataTable({
        responsive: true, //se adapta la tabla
        destroy: true, //se puede reinicializar con otro proceso
        deferRender: true, //
        language: {
                    "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json"
        },
        ajax: {
            url: window.location.pathname, //
            type: 'POST',
            data: {
                'action': 'load_plantas'
            }, //parametros
            dataSrc: "" //tengo datos con una variable
        },
        aoColumns: [ //columnas de las tablas, se debe poner los campos del models.py
            {"data": "id"},
            {"data": "nombre"},
            {"data": "descripcion"},
            {"data": "tiempo_produccion"},
            {"data": null},
        ],
        columnDefs: [ //Por columna lo puedes personalizar
            {
                targets: [-1], //voy de atras hacia arriba
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    //buttons: me creo mis botones con html, recuerda que estoy accediendo mediante objetos
                    var buttons = '<a href="/gestion-riego/plantas/update/' + row.id + '/" class="btn btn-secondary"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/gestion-riego/plantas/delete/' + row.id + '/" class="btn btn-secondary"><i class="fas fa-trash-alt"></i></a>'
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {
            //aqui va alguna funcion que se ejecutara despues de cargar la tabla
        }
    });
}

$(function () {
    loadPlantas();
});