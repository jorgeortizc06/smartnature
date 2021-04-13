function loadSensores() {
    $('#data').DataTable({
        responsive: true, //se adapta la tabla
        autoWidth: false, //respeta el ancho de mi tabla
        destroy: true, //se puede reinicializar con otro proceso
        deferRender: true, //
        language: {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json"
        },
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
            {"data": "tipo_sensor"},
            {"data": "fecha_registro"},
            {"data": "value"},
            {"data": "estado"},
            {"data": "device"},
            {"data": null},
        ],
        columnDefs: [ //Por columna lo puedes personalizar
            {
                targets: [-1], //voy de atras hacia arriba
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    //buttons: me creo mis botones con html, recuerda que estoy accediendo mediante objetos
                    var buttons = '<a href="/gestion-riego/sensores/update/' + row.id + '/" class="btn btn-primary"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/gestion-riego/sensores/delete/' + row.id + '/" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a>'
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
        initComplete: function (settings, json) {
            //aqui va alguna funcion que se ejecutara despues de cargar la tabla
        }
    });
}

function loadSensoresCharts() {
    var optionsHumedadSuelo = {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Sensor de Humedad de Suelo'
        },
        subtitle: {
            text: 'Historial por Día: ' + mes,
        },
        xAxis: {
            categories: [
                1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30
            ],
            crosshair: true
        },
        yAxis: {
            min: 0,
            title: {
                text: 'puntos'
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.1f} puntos</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [{
            name: 'Sensor 1',
            data: sensor_humedad_suelo_1_avgs

        },
            {
                name: 'Sensor 2',
                data: sensor_humedad_suelo_2_avgs

            },
            {
                name: 'Sensor 3',
                data: sensor_humedad_suelo_3_avgs,

            },
            {
                name: 'Sensor 4',
                data: sensor_humedad_suelo_4_avgs,

            }]
    };

    var optionsHumedadAmbiente = {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Sensor de Humedad Ambiente'
        },
        subtitle: {
            text: 'Historial por Día: {{mes}}'
        },
        xAxis: {
            categories: [
                1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30
            ],
            crosshair: true
        },
        yAxis: {
            min: 0,
            title: {
                text: '%'
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.1f} %</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [{
            name: 'Sensor 1',
            colorByPoint: true,
            data: sensor_humedad_ambiente_1_avgs

        }]
    };
    var optionsTemperaturaAmbiente = {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Sensor de Temperatura Ambiente'
        },
        subtitle: {
            text: 'Historial por Día: {{mes}}'
        },
        xAxis: {
            categories: [
                1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30
            ],
            crosshair: true
        },
        yAxis: {
            min: 0,
            title: {
                text: 'oC'
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.1f} oC</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [{
            name: 'Sensor 1',
            colorByPoint: true,
            data: sensor_temperatura_ambiente_1_avgs

        }]
    }
    var highHumedadSuelo = Highcharts.chart('c_sensor_humedad_suelo', optionsHumedadSuelo);
    var highTemperaturaAmbiente = Highcharts.chart('c_sensor_temperatura_ambiente', optionsTemperaturaAmbiente);
    var highHumedadAmbiente = Highcharts.chart('c_sensor_humedad_ambiente', optionsHumedadAmbiente);
}

function searchSensoresForDateAjax() {
    var optionsNewHumedadSuelo = {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Sensor de Humedad de Suelo'
        },
        subtitle: {},
        xAxis: {
            categories: [
                1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31
            ],
            crosshair: true
        },
        yAxis: {
            min: 0,
            title: {
                text: 'puntos'
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.1f} puntos</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: []
    }
    var optionsNewTemperaturaAmbiente = {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Sensor de Temperatura Ambiental'
        },
        subtitle: {},
        xAxis: {
            categories: [
                1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31
            ],
            crosshair: true
        },
        yAxis: {
            min: 0,
            title: {
                text: 'oC'
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.1f} oC</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: []
    }
    var optionsNewHumedadAmbiente = {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Sensor de Humedad Ambiental'
        },
        subtitle: {},
        xAxis: {
            categories: [
                1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31
            ],
            crosshair: true
        },
        yAxis: {
            min: 0,
            title: {
                text: '%'
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.1f} %</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: []
    }

    $('#dateForChart').on('change', function () {
        var fecha = $(this).val();
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'search_historial_sensores_month',
                'fecha': fecha
            },
            dataType: 'json',
        }).done(function (data) {
            //console.log(data);
            //var dia = new Highcharts.chart('container4', options1);
            var newHighHumedadSuelo = new Highcharts.chart('c_sensor_humedad_suelo', optionsNewHumedadSuelo);
            newHighHumedadSuelo.addSeries({
                name: 'Sensor 1',
                data: data.sensor_humedad_suelo_1_avgs
            })
            newHighHumedadSuelo.addSeries({
                name: 'Sensor 2',
                data: data.sensor_humedad_suelo_2_avgs
            })
            newHighHumedadSuelo.addSeries({
                name: 'Sensor 3',
                data: data.sensor_humedad_suelo_3_avgs
            })
            newHighHumedadSuelo.addSeries({
                name: 'Sensor 4',
                data: data.sensor_humedad_suelo_4_avgs
            })
            newHighHumedadSuelo.setSubtitle({
                text: 'Historial por Día:' + data.mes
            });
            var newHighTemperaturaAmbiente = Highcharts.chart('c_sensor_temperatura_ambiente', optionsNewTemperaturaAmbiente);
            newHighTemperaturaAmbiente.addSeries({
                name: 'Sensor 1',
                colorByPoint: true,
                data: data.sensor_temperatura_ambiente_1_avgs
            })
            newHighTemperaturaAmbiente.setSubtitle({
                text: 'Historial por Día:' + data.mes
            });
            var newHighHumedadAmbiente = Highcharts.chart('c_sensor_humedad_ambiente', optionsNewHumedadAmbiente);
            newHighHumedadAmbiente.addSeries({
                name: 'Sensor 1',
                colorByPoint: true,
                data: data.sensor_humedad_ambiente_1_avgs
            })
            newHighHumedadAmbiente.setSubtitle({
                text: 'Historial por Día:' + data.mes
            });

            return false;
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {
        });
    });

    $('#dateForDatable').on('change', function () {
        var fecha = $(this).val();
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'search_historial_sensores_month_datatable',
                'fecha': fecha
            },
            dataType: 'json',
        }).done(function (data) {
            var table = $('#data').DataTable();
            table.clear();
            var newTable = $('#data').DataTable({
                destroy: true,
                data: data,
                responsive: true,
                language: {
                    "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json"
                },
                columns: [ //columnas de las tablas, se debe poner los campos del models.py
                    {"data": "id"},
                    {"data": "codigo_sensor"},
                    {"data": "tipo_sensor"},
                    {"data": "fecha_registro"},
                    {"data": "value"},
                    {"data": "estado"},
                    {"data": "device"},
                    {"data": null},
                ],
                columnDefs: [ //Por columna lo puedes personalizar
                    {
                        targets: [-1], //voy de atras hacia arriba
                        class: 'text-center',
                        orderable: false,
                        render: function (data, type, row) {
                            //buttons: me creo mis botones con html, recuerda que estoy accediendo mediante objetos
                            var buttons = '<a href="/gestion-riego/sensores/update/' + row.id + '/" class="btn btn-primary"><i class="fas fa-edit"></i></a> ';
                            buttons += '<a href="/gestion-riego/sensores/delete/' + row.id + '/" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a>'
                            return buttons;
                        }
                    },
                ],
                initComplete: function (settings, json) {
                    //aqui va alguna funcion que se ejecutara despues de cargar la tabla
                }
            });
        });
    });
}
$(function () {
    loadSensoresCharts();
    loadSensores();
    searchSensoresForDateAjax();

});