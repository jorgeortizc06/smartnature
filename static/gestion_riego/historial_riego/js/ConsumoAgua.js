function loadConsumoAguaForMonth() {
    $('#table_uso_agua').DataTable({
        destroy: true, //se puede reinicializar con otro proceso
        deferRender: true, //
        language: {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json"
        },
        ajax: {
            url: window.location.pathname, //
            type: 'POST',
            data: {
                'action': 'load_consumo_agua'
            }, //parametros
            dataSrc: "" //tengo datos con una variable
        },
        columns: [ //columnas de las tablas, se debe poner los campos del models.py
            {"data": "dia"},
            {"data": "tiempo_riego_1_variable"},
            {"data": "consumo_agua_1_variable"},
            {"data": "tiempo_riego_3_variable"},
            {"data": "consumo_agua_3_variable"},
            {"data": "tiempo_riego_4_variable"},
            {"data": "consumo_agua_4_variable"}
            //{"data": "persona"},
            //{"data": "tipo_logica_difusa"},
            //{"data": "tipo_rol"},
        ],
        order: [[0, 'desc']],
        initComplete: function (settings, json) {
            //aqui va alguna funcion que se ejecutara despues de cargar la tabla
        }

    });
}

function loadChartConsumoAguaForMonth() {
    var options_consumo_agua_1_variable = {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Consumo de Agua'
        },
        subtitle: {
            text: 'Mes de ' + mes,
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
                text: 'LITROS'
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.1f} litros</b></td></tr>',
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
            name: '1 Variable',
            data: consumo_agua_1_variable

        },
            {
                name: '3 variables',
                data: consumo_agua_3_variable

            },
            {
                name: '4 Variables',
                data: consumo_agua_4_variable

            }]
    };

    var highHumedadSuelo = Highcharts.chart('c_consumo_agua_1_variable', options_consumo_agua_1_variable);
}

function searchForDateConsumoAgua() {
//Para ajax
    var options_new_consumo_agua_1_variable = {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Consumo de Agua'
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
                text: 'LITROS'
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.1f} litros</b></td></tr>',
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

    $('#dateMes').on('change', function () {
        var fecha = $(this).val();
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'search_consumo_agua_month',
                'fecha': fecha
            },
            dataType: 'json',
        }).done(function (data) {

            $('#consumo_agua').html('Tipo de lógica digusa de 1 variable:' + data.consumo_agua_1_variable_mensual + '<br> Tipo de lógica difusa de 3 variables: ' + data.consumo_agua_3_variable_mensual + '<br> Tipo de lógica difusa de 4 variables: ' + data.consumo_agua_4_variable_mensual);
            //var dia = new Highcharts.chart('container4', options1);
            var newHighConsumoAgua = new Highcharts.chart('c_consumo_agua_1_variable', options_new_consumo_agua_1_variable);
            newHighConsumoAgua.addSeries({
                name: '1 Variable',
                data: data.consumo_agua_1_variable
            })
            newHighConsumoAgua.addSeries({
                name: '3 variables',
                data: data.consumo_agua_3_variable
            })
            newHighConsumoAgua.addSeries({
                name: '4 Variables',
                data: data.consumo_agua_4_variable
            })

            newHighConsumoAgua.setSubtitle({
                text: 'Consumo de agua:' + data.mes
            });

            var table = $('#table_uso_agua').DataTable();
            table.clear();
            var newTable = $('#table_uso_agua').DataTable({
                destroy: true, //se puede reinicializar con otro proceso
                deferRender: true, //
                language: {
                    "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json"
                },
                data: data.consumo_agua_months,
                columns: [ //columnas de las tablas, se debe poner los campos del models.py
                    {"data": "dia"},
                    {"data": "tiempo_riego_1_variable"},
                    {"data": "consumo_agua_1_variable"},
                    {"data": "tiempo_riego_3_variable"},
                    {"data": "consumo_agua_3_variable"},
                    {"data": "tiempo_riego_4_variable"},
                    {"data": "consumo_agua_4_variable"}
                ],
                order: [[0, 'desc']],
                initComplete: function (settings, json) {
                    //aqui va alguna funcion que se ejecutara despues de cargar la tabla
                }

            });


            return false;
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {
        });
    });
}

$(function () {
    loadConsumoAguaForMonth();
    loadChartConsumoAguaForMonth();
    searchForDateConsumoAgua();
})