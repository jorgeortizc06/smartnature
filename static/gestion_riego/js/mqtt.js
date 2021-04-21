var MQTTbroker = "192.168.0.254";
var MQTTport = 8083
var MQTTsubTopic = "device1/#"
var chart; // global variuable for chart
var dataTopics = new Array();
var humedadSueloTopics = new Array();
var gSensorTemperatura1 = new JustGage({
    id: "SensorTemperatura1",
    min: 0,
    max: 50,
    title: "Temperatura Ambiental oC"
});
var gSensorHumedad1 = new JustGage({
    id: "SensorHumedad1",
    min: 0,
    max: 100,
    title: "Humedad Ambiental %"
});
var gSensorCaudal1 = new JustGage({
    id: "SensorCaudal1",
    min: 0,
    max: 30,
    title: "Caudal de Agua en Litros"
});
var gSensorConsumoAgua1 = new JustGage({
    id: "SensorConsumoAgua1",
    min: 0,
    max: 300,
    title: "Consumo de Agua en Litros"
});
var gSensorSuelo1 = new JustGage({
    id: "SensorSuelo1",
    min: 0,
    max: 1024,
    title: "Humedad del Suelo 1"
});
var gSensorSuelo2 = new JustGage({
    id: "SensorSuelo2",
    min: 0,
    max: 1024,
    title: "Humedad del Suelo 2"
});
var gSensorSuelo3 = new JustGage({
    id: "SensorSuelo3",
    min: 0,
    max: 1024,
    title: "Humedad del Suelo 3"
});
var gSensorSuelo4 = new JustGage({
    id: "SensorSuelo4",
    min: 0,
    max: 1024,
    title: "Humedad del Suelo 4"
});
var chartSensorAmbientalCaudal = new Highcharts.Chart({
    chart: {
        renderTo: 'containerSensorAmbientalCaudal',
        defaultSeriesType: 'spline'
    },
    title: {
        text: 'Sensores ambientales y Consumo de Agua'
    },
    subtitle: {
        text: 'broker: ' + MQTTbroker + ' | port: ' + MQTTport + ' | topic : ' + MQTTsubTopic
    },
    xAxis: {
        type: 'datetime',
        tickPixelInterval: 300,
        maxZoom: 20 * 1000
    },
    yAxis: {
        minPadding: 0.2,
        maxPadding: 0.2,
        title: {
            text: 'Value',
            margin: 80
        }
    },
    series: []
});
// called when the client connects
function onConnect() {
    // Once a connection has been made, make a subscription and send a message.
    console.log("onConnect");
    client.subscribe("device1/#");
    message = new Paho.MQTT.Message("Hello");
    message.destinationName = "World";
    client.send(message);
}


// called when the client loses its connection
function onConnectionLost(responseObject) {
    if (responseObject.errorCode !== 0) {
        console.log("onConnectionLost:" + responseObject.errorMessage);
    }
}

//Verifica si es un numero real
function isNumber(n) {
    return !isNaN(parseFloat(n)) && isFinite(n);
}

//Grafico las figuras de los sensores de justgage
function graficarJustGageSensores(destinationName, payloadString) {
    if (destinationName == 'device1/sensorTemperatura1') {
        gSensorTemperatura1.refresh(payloadString);
    } else if (destinationName == 'device1/sensorHumedad1') {
        gSensorHumedad1.refresh(payloadString);
    } else if (destinationName == 'device1/sensorCaudal1') {
        gSensorCaudal1.refresh(payloadString);
    } else if (destinationName == 'device1/sensorConsumoAgua1') {
        gSensorConsumoAgua1.refresh(payloadString);
    } else if (destinationName == 'device1/sensorSuelo1') {
        gSensorSuelo1.refresh(payloadString);
    } else if (destinationName == 'device1/sensorSuelo2') {
        gSensorSuelo2.refresh(payloadString);
    } else if (destinationName == 'device1/sensorSuelo3') {
        gSensorSuelo3.refresh(payloadString);
    } else if (destinationName == 'device1/sensorSuelo4') {
        gSensorSuelo4.refresh(payloadString);
    } else {
        console.log("No hay topico para justgage: " + payloadString);
    }
}

//Graficar charts para sensor de temperatura y humedad ambiental, caudal y consumo de agua, humedad de suelo
function graficarChartsSensores(destinationName, payloadString) {
    //Visualizo en un chart solamente los sensores temperatura y humedad ambiental, caudal y consumo de agua


    if (dataTopics.indexOf(destinationName) < 0) {
        dataTopics.push(destinationName); //add new topic to array
        var y = dataTopics.indexOf(destinationName); //get the index no
        //create new data series for the chart
        var newseries = {
            id: y,
            name: destinationName,
            data: []
        }
        chartSensorAmbientalCaudal.addSeries(newseries); //add the series
    }

    var y = dataTopics.indexOf(destinationName); //get the index no of the topic from the array
    var myEpoch = new Date().getTime(); //get current epoch time
    var thenum = payloadString.replace(/^\D+/g, ''); //remove any text spaces from the message
    var plotMqtt = [myEpoch, Number(thenum)]; //create the array

    if (isNumber(thenum)) { //check if it is a real number and not text
        //console.log('is a propper number, will send to chart.')
        //console.log(plotMqtt +' '+y)
        plotSensorAmbientalCaudal(plotMqtt, y);	//send it to the plot function
    }

}

function plotSensorAmbientalCaudal(point, chartno) {
    var series = chartSensorAmbientalCaudal.series[0],
        shift = series.data.length > 20; // shift if the series is
    console.log("Series", series);

    // longer than 20
    // add the point
    chartSensorAmbientalCaudal.series[chartno].addPoint(point, true, shift);
};

function plotSensorHumedadSuelo(point, chartno) {
    var series = chartSensorHumedadSuelo.series[0],
        shift = series.data.length > 20; // shift if the series is
    // longer than 20
    // add the point
    console.log("Series", series);

    chartSensorHumedadSuelo.series[chartno].addPoint(point, true, shift);
};

// called when a message arrives
function onMessageArrived(message) {
    graficarJustGageSensores(message.destinationName, message.payloadString);
    graficarChartsSensores(message.destinationName, message.payloadString);
}


$(function () {
    // Create a client instance
    client = new Paho.MQTT.Client(MQTTbroker, MQTTport, "clientId");
    // Set callback handlers
    client.onConnectionLost = onConnectionLost;
    // Mensajes
    client.onMessageArrived = onMessageArrived;
    var options = {
        timeout: 3,
        useSSL: false,
        onSuccess: function () {
            console.log("mqtt connected");
            // Connection succeeded; subscribe to our topics
            client.subscribe("device1/#", {qos: 1});
        },
        onFailure: function (message) {
            console.log("Connection failed, ERROR: " + message.errorMessage);
            //window.setTimeout(location.reload(),20000); //wait 20seconds before trying to connect again.
        }
    };
    // Connect the client
    client.connect(options)
    function OnOff(dato) {
        message = new Paho.MQTT.Message(dato);
        message.destinationName = 'device1/electrovalvula'
        if (dato == "ON") {
            document.getElementById("estado").textContent = "activado";
        } else {
            document.getElementById("estado").textContent = "desactivado";
        }
        client.send(message);
    };

    $('#on').click(function () {
        OnOff('ON')
    })

    $('#off').click(function () {
        OnOff('OFF')
    })
});