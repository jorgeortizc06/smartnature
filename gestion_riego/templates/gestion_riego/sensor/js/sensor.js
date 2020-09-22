var gaugeOptions = {
    chart: {
        type: 'solidgauge'
    },

    title: null,

    pane: {
        center: ['50%', '85%'],
        size: '140%',
        startAngle: -90,
        endAngle: 90,
        background: {
            backgroundColor:
                Highcharts.defaultOptions.legend.backgroundColor || '#EEE',
            innerRadius: '60%',
            outerRadius: '100%',
            shape: 'arc'
        }
    },

    exporting: {
        enabled: false
    },

    tooltip: {
        enabled: false
    },

    // the value axis
    yAxis: {
        stops: [
            [0.1, '#55BF3B'], // green
            [0.5, '#DDDF0D'], // yellow
            [0.9, '#DF5353'] // red
        ],
        lineWidth: 0,
        tickWidth: 0,
        minorTickInterval: null,
        tickAmount: 2,
        title: {
            y: -70
        },
        labels: {
            y: 16
        }
    },

    plotOptions: {
        solidgauge: {
            dataLabels: {
                y: 5,
                borderWidth: 0,
                useHTML: true
            }
        }
    }
};

// The speed gauge
var chartTempAmbiental = Highcharts.chart('container-speed', Highcharts.merge(gaugeOptions, {
    yAxis: {
        min: 0,
        max: 100,
        title: {
            text: 'Temperatura Ambiental'
        }
    },

    credits: {
        enabled: false
    },

    series: [{
        name: 'TemperaturaAmbiental',
        data: [20],
        dataLabels: {
            format:
                '<div style="text-align:center">' +
                '<span style="font-size:25px">{y}</span><br/>' +
                '<span style="font-size:12px;opacity:0.4">oC</span>' +
                '</div>'
        },
        tooltip: {
            valueSuffix: ' oC'
        }
    }]

}));

// The RPM gauge
var chartHumedAmbiente = Highcharts.chart('container-rpm', Highcharts.merge(gaugeOptions, {
    yAxis: {
        min: 0,
        max: 100,
        title: {
            text: 'Humedad Ambiental'
        }
    },

    series: [{
        name: 'HumedadAmbiental',
        data: [20],
        dataLabels: {
            format:
                '<div style="text-align:center">' +
                '<span style="font-size:25px">{y:.1f}</span><br/>' +
                '<span style="font-size:12px;opacity:0.4">' +
                '* %' +
                '</span>' +
                '</div>'
        },
        tooltip: {
            valueSuffix: '%'
        }
    }]

}));

// Bring life to the dials
setInterval(function () {
    // Speed
    var point,
        newVal,
        inc;

    if (chartTempAmbiental) {
        point = chartTempAmbiental.series[0].points[0];
        
        
        newVal = {{temp_ambiental}};
        

        point.update(newVal);
    }
}, 2000);

// Bring life to the dials
setInterval(function () {
    // Speed
    var point,
        newVal,
        inc;

    if (chartHumedAmbiente) {
        point = chartHumedAmbiente.series[0].points[0];
        
        
        newVal = {{humed_ambiental}};
        
        console.log(newVal);
        point.update(newVal);
    }
}, 2000);