$(function () {
    $('#table_plataformas').DataTable({
        responsive: true, //se adapta la tabla
        autoWidth: false, //respeta el ancho de mi tabla
        destroy: true, //se puede reinicializar con otro proceso
        deferRender: true, //
        ajax: {
            url: window.location.pathname, //
            type: 'POST',
            data: {
                'action': 'load_plataformas'
            }, //parametros
            dataSrc: "" //tengo datos con una variable
        },
        columns: [ //columnas de las tablas, se debe poner los campos del models.py
            {"data": "id"},
            {"data": "nombre"},
            {"data": "descripcion"},
            {"data": "horario1"},
            {"data": "horario2"},
            {"data": "horario3"},
            {"data": "tipo_suelo"},
            {"data": "device"},
            {"data": "Opciones"},
        ],
        columnDefs: [ //Por columna lo puedes personalizar
            {
                targets: [-1], //voy de atras hacia arriba
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    //buttons: me creo mis botones con html, recuerda que estoy accediendo mediante objetos
                    var buttons = '<a href="/gestion_riego/plataforma_update/' + row.id + '/" class="btn btn-secondary"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/gestion_riego/plataforma_delete/' + row.id + '/" class="btn btn-secondary"><i class="fas fa-trash-alt"></i></a>'
                    return buttons;
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
});