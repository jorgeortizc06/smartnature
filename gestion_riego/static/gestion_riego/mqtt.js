var MQTTbroker = document.getElementById("iptxt").value;
    var MQTTport = parseInt(document.getElementById("puertotxt").value);
    var MQTTsubTopic = document.getElementById("topictxt").value; //works with wildcard # and + topics dynamically now
    var chart; // global variuable for chart
    var dataTopics = new Array();
    var humedadSueloTopics = new Array();
    //mqtt broker
    var client = new Paho.MQTT.Client(MQTTbroker, MQTTport,
        "myclientid_" + parseInt(Math.random() * 100, 10));
    client.onMessageArrived = onMessageArrived;
    client.onConnectionLost = onConnectionLost;

    //mqtt connecton options including the mqtt broker subscriptions
    var options = {
        timeout: 3,
        onSuccess: function () {
            console.log("mqtt connected");
            // Connection succeeded; subscribe to our topics
            client.subscribe(MQTTsubTopic, { qos: 1 });
        },
        onFailure: function (message) {
            console.log("Connection failed, ERROR: " + message.errorMessage);
            //window.setTimeout(location.reload(),20000); //wait 20seconds before trying to connect again.
        }
    };
    //can be used to reconnect on connection lost
    function onConnectionLost(responseObject) {
        console.log("connection lost: " + responseObject.errorMessage);
        //window.setTimeout(location.reload(),20000); //wait 20seconds before trying to connect again.
    };
    //what is done when a message arrives from the broker
    function onMessageArrived(message) {
        console.log(message.destinationName, '', message.payloadString);
        //check if it is a new topic, if not add it to the array
        if(message.destinationName == 'device1/sensorTemperatura1' || message.destinationName == 'device1/sensorHumedad1' || message.destinationName == 'device1/sensorCaudal1' || message.destinationName == 'device1/sensorConsumoAgua1'){
            if (dataTopics.indexOf(message.destinationName) < 0) {
                
                    dataTopics.push(message.destinationName); //add new topic to array
                    var y = dataTopics.indexOf(message.destinationName); //get the index no

                    //create new data series for the chart
                    var newseries = {
                        id: y,
                        name: message.destinationName,
                        data: []
                    };
                    chart.addSeries(newseries); //add the series
                
            };

            var y = dataTopics.indexOf(message.destinationName); //get the index no of the topic from the array
            var myEpoch = new Date().getTime(); //get current epoch time
            var thenum = message.payloadString.replace(/^\D+/g, ''); //remove any text spaces from the message
            var plotMqtt = [myEpoch, Number(thenum)]; //create the array
            if (isNumber(thenum)) { //check if it is a real number and not text
                console.log('is a propper number, will send to chart.')
                plot(plotMqtt, y);	//send it to the plot function
            };
        }else{
            if (humedadSueloTopics.indexOf(message.destinationName) < 0) {
                
                humedadSueloTopics.push(message.destinationName); //add new topic to array
                    var y = humedadSueloTopics.indexOf(message.destinationName); //get the index no

                    //create new data series for the chart
                    var newseries = {
                        id: y,
                        name: message.destinationName,
                        data: []
                    };
                    chart2.addSeries(newseries); //add the series
                
            };

            var y = humedadSueloTopics.indexOf(message.destinationName); //get the index no of the topic from the array
            var myEpoch = new Date().getTime(); //get current epoch time
            var thenum = message.payloadString.replace(/^\D+/g, ''); //remove any text spaces from the message
            var plotMqtt = [myEpoch, Number(thenum)]; //create the array
            if (isNumber(thenum)) { //check if it is a real number and not text
                console.log('is a propper number, will send to chart.')
                plot1(plotMqtt, y);	//send it to the plot function
            };
        };
    };
    //check if a real number
    function isNumber(n) {
        return !isNaN(parseFloat(n)) && isFinite(n);
    };
    //function that is called once the document has loaded
    function init() {
        //i find i have to set this to false if i have trouble with timezones.
        Highcharts.setOptions({
            global: {
                useUTC: false
            }
        });
        // Connect to MQTT broker
        client.connect(options);
    };
    //this adds the plots to the chart
    function plot(point, chartno) {
        console.log("Punto: " + point);

        var series = chart.series[0],
            shift = series.data.length > 20; // shift if the series is
        // longer than 20
        // add the point
        chart.series[chartno].addPoint(point, true, shift);
    };
    function plot1(point, chartno) {
        console.log("Punto: " + point);

        var series = chart.series[0],
            shift = series.data.length > 20; // shift if the series is
        // longer than 20
        // add the point
        chart2.series[chartno].addPoint(point, true, shift);
    };
    //settings for the chart
    $(document).ready(function () {
        
        chart = new Highcharts.Chart({
            chart: {
                renderTo: 'container',
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

        chart2 = new Highcharts.Chart({
            chart: {
                renderTo: 'container2',
                defaultSeriesType: 'spline'
            },
            title: {
                text: 'Sensores de Humedad'
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
        

    });
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