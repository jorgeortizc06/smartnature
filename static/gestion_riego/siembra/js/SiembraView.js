function loadSiembras() {
    $('#table_siembras').DataTable({
        responsive: true, //se adapta la tabla
        autoWidth: false, //respeta el ancho de mi tabla
        destroy: true, //se puede reinicializar con otro proceso
        deferRender: true, //
        ajax: {
            url: window.location.pathname, //
            type: 'POST',
            data: {
                'action': 'load_siembras'
            }, //parametros
            dataSrc: "" //tengo datos con una variable
        },
        columns: [ //columnas de las tablas, se debe poner los campos del models.py
            {"data": "id"},
            {"data": "fecha_siembra"},
            {"data": "cantidad_plantas"},
            {"data": "distancia_siembra"},
            {"data": "plataforma"},
            {"data": "planta"},
            {"data": null},
        ],
        columnDefs: [ //Por columna lo puedes personalizar
            {
                targets: [-1], //voy de atras hacia arriba
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    //buttons: me creo mis botones con html, recuerda que estoy accediendo mediante objetos
                    var buttons = '<a href="/gestion-riego/siembras/update/' + row.id + '/" class="btn btn-secondary"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/gestion-riego/siembras/delete/' + row.id + '/" class="btn btn-secondary"><i class="fas fa-trash-alt"></i></a>'
                    return buttons;
                }
            },
        ],
        order: [[0, 'desc']],
        initComplete: function (settings, json) {
            //aqui va alguna funcion que se ejecutara despues de cargar la tabla
        }
    });
}

$(function () {
    loadSiembras();
});