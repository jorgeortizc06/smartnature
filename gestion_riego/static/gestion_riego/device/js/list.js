var tblDevice;

function getData(){
    //Me ayuda a cargas datos con la libreria DataTable
    tblDevice = $('#data').DataTable({
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
            {"data": "Opciones"},
        ],
        columnDefs: [ //Por columna lo puedes personalizar
            {
                targets: [-1], //voy de atras hacia arriba
                class: 'text-center',
                orderable: false,
                render: function(data, type, row) {
                    //buttons: me creo mis botones con html, recuerda que estoy accediendo mediante objetos
                    var buttons = '<a href="#" class="btn btn-secondary btnEdit"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="#" rel="btnDelete" class="btn btn-secondary"><i class="fas fa-trash-alt"></i></a>'
                    return buttons;
                }
            },
        ],
        order: [[0, 'desc']], //ordeno la primera columna descendente
        initComplete: function(settings, json){
            //aqui va alguna funcion que se ejecutara despues de cargar la tabla
        }
    });
}

//Funcion para trabajar con modals
$(function() {  //esta es la funciona anonima abreviada de $(document).ready(function(){});
    modal_title = $('.modal-title'); //titulo del modal
    getData(); //cargo mi datatable
    $('.btnAdd').click(function(){ //al hacer clic en nuevo visualizo el modal
        $('input[name="action"]').val('add');
        //personalizo mi titulo del modal
        modal_title.find('span').html('Nuevo Dispositivo');
        modal_title.find('i').removeClass().addClass('fas fa-plus');
        //veo mi modal
        $('#modalDevice').modal('show');
    })
    //Me ayuda a cargar datos al model de una fila de la tabla con el boton edit
    $('#data tbody')
        .on('click', '.btnEdit', function(){
        //personalizo mi titulo del modal
        modal_title.find('span').html('Editar Dispositivo');
        modal_title.find('i').removeClass().addClass('fas fa-edit');
        //Recupero los datos de la fila
        var data = tblDevice.row($(this).parents('tr')).data();
        //lo cargo al modal
        $("input[name='action']").val('edit');
        $("input[name='id']").val(data.id);
        $("input[name='nombre']").val(data.nombre);
        $("input[name='descripcion']").val(data.descripcion);
        $("input[name='ip']").val(data.ip);
        $("input[name='topic']").val(data.topic);
        $("input[name='puerto']").val(data.puerto);
        $('#modalDevice').modal('show');
    })
        .on('click', 'a[rel="btnDelete"]', function(){
            var data = tblDevice.row($(this).parents('tr')).data();
            var parameters = new FormData();
            parameters.append('action', 'delete');
            parameters.append('id', data.id);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de eliminar el registro: '+data.nombre+'?', parameters, function () {
                $('#modalDevice').modal('hide'); //guarda y se oculta el modal
                tblDevice.ajax.reload(); //recarga mi tabla
            });
    });

    //Metodo para limpiar datos cuando oculto el modal
    $('#modalDevice').on('show.bs.modal', function(){
        $('form')[0].reset(); //aun no me funciona, no se el porque
    });

    $('form').on('submit', function (e) { //en el modal al momento de poner guardar me sale esta alerta
        e.preventDefault();
        var parameters = new FormData(this);
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            $('#modalDevice').modal('hide'); //guarda y se oculta el modal
            tblDevice.ajax.reload(); //recarga mi tabla
        });
    });

});