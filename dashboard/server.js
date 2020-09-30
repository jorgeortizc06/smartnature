const mqtt = require('mqtt')
var fs = require('fs');
var express = require('express');

//Initialization
var app = express();

// Solution to bypass firewall restrictions with port 1883
const MQTT_SERVER = '192.168.0.6'
const MQTT_PORT = 1883

const MQTT_TOPIC_TEMPERATURE = 'casa/sala/SensorTemperatura1'
const MQTT_TOPIC_HUMIDITY = 'casa/sala/SensorHumedad1'
const MQTT_TOPIC_SUELO = 'casa/sala/SensorSuelo1'

var client  = mqtt.connect('mqtt://' + MQTT_SERVER + ":" + MQTT_PORT)

var app = express();
var server = app.listen(3000);
var io = require('socket.io').listen(server);

app.use(express.static(__dirname + '/public'));

app.get('/',  (req, res) => {
  fs.readFile(__dirname + '/public/index.html', (error, data) => {
    if (error) {
      res.writeHead(404);
      res.write("Not Found");
      res.end();
    } else {
      res.writeHead(200);
      res.write(data, "utf8");
      res.end();
    }
  });
});

io.sockets.on('connection', (socket) => {
});

client.on('connect',  () => {
  client.subscribe(MQTT_TOPIC_TEMPERATURE);
  client.subscribe(MQTT_TOPIC_HUMIDITY);
  client.subscribe(MQTT_TOPIC_SUELO);
})  

client.on('message', function (topic, message) {
  console.log(topic);
  console.log(message.toString());

  if (topic == MQTT_TOPIC_TEMPERATURE) {
    io.sockets.emit('temperature', { raw: message.toString() });
  }

  if (topic == MQTT_TOPIC_HUMIDITY) {
    io.sockets.emit('humidity', { raw: message.toString() });
  }
  if (topic == MQTT_TOPIC_SUELO) {
    io.sockets.emit('suelo', { raw: message.toString() });
  }
})

console.log('Server app listening on port 3000...');