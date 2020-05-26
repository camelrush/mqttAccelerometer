// constants
var MQTT_TOPIC_SUB = 'mqttAccelerometer'   // Mqtt Toic(subscribe)

// variables
var mqtt_client;

var ax_val = 0;
var ay_val = 0;
var az_val = 0;

var chartColors = {
    red: 'rgb(255, 99, 132)',
    orange: 'rgb(255, 159, 64)',
    yellow: 'rgb(255, 205, 86)',
    green: 'rgb(75, 192, 192)',
    blue: 'rgb(54, 162, 235)',
    purple: 'rgb(153, 102, 255)',
    grey: 'rgb(201, 203, 207)'
};

// Docuent Ready Event
$(document).ready(function() {

    // Set Signature To URL
    // ★★ ここにAccessId、SecretKeyを設定 ★★
    var credentials = {};
    credentials.accessKeyId = '';
    credentials.secretAccessKey = '';
    var requestUrl = SigV4Utils.getSignedUrl('xxxxxxxxxxxxxx-xxx.iot.ap-northeast-1.amazonaws.com', 'ap-northeast-1', credentials);

    // Connect to Mqtt Broker(on AWS)
    var clientId = 'awss3_controller';
    mqtt_client = new Paho.Client(requestUrl, clientId);
    var connectOptions = {
        useSSL: true,
        timeout: 3,
        mqttVersion: 4,
        onSuccess: mqtt_onConnect
    };
    mqtt_client.connect(connectOptions);
    mqtt_client.onMessageArrived = mqtt_onMessageArrived;
    mqtt_client.onConnectionLost = mqtt_onConnectionLost;

});

function onRefresh(chart) {
    chart.config.data.datasets[0].data.push({x: Date.now(),y: ax_val});
    chart.config.data.datasets[1].data.push({x: Date.now(),y: ay_val});
    chart.config.data.datasets[2].data.push({x: Date.now(),y: az_val});
}

var color = Chart.helpers.color;
var config = {
    type: 'line',
    data: {
        datasets: [{
            label: 'ax',
            backgroundColor: color(chartColors.red).alpha(0.5).rgbString(),
            borderColor: chartColors.red,
            fill: false,
            cubicInterpolationMode: 'monotone',
            data: []
        }, {
            label: 'ay',
            backgroundColor: color(chartColors.blue).alpha(0.5).rgbString(),
            borderColor: chartColors.blue,
            fill: false,
            cubicInterpolationMode: 'monotone',
            data: []
        }, {
            label: 'az',
            backgroundColor: color(chartColors.green).alpha(0.5).rgbString(),
            borderColor: chartColors.green,
            fill: false,
            cubicInterpolationMode: 'monotone',
            data: []
        }]
    },
    options: {
        title: {
            display: true,
            text: '3軸加速度センサー チャート'
        },
        scales: {
            xAxes: [{
                type: 'realtime',
                realtime: {
                    duration: 5000,
                    refresh: 50,
                    delay: 300,
                    onRefresh: onRefresh
                }
            }],
            yAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: 'value'
                },
                position:'right',
                ticks:{min:-3.5,max:3.5}
            }]
        },
        tooltips: {
            mode: 'nearest',
            intersect: false
        },
        hover: {
            mode: 'nearest',
            intersect: false
        }
    }
};

window.onload = function() {
    var ctx = document.getElementById('myChart').getContext('2d');
    window.myChart = new Chart(ctx, config);
};

// mqtt Connected Event Handler
function mqtt_onConnect()
{
    // Entry Mqtt Subscribe.
    mqtt_client.subscribe(MQTT_TOPIC_SUB);

    // Button Display Change. 
    $('#btn-connect').val('DisConnect');
	console.log('connected');
}

// MQTT MessageArrived Event Handler
function mqtt_onMessageArrived(msg)
{
    var msg_json = JSON.parse(msg.payloadString);
    ax_val = msg_json.ax;
    ay_val = msg_json.ay;
    az_val = msg_json.az;
}

// MQTT ConnectionLost Event Handler
function mqtt_onConnectionLost(responseObject) 
{
    // Error Case
    if (responseObject.errorCode !== 0) {
        console.log('onConnectionLost:'+responseObject.errorMessage);
        return;
    }

    // Button Display Change. 
    $('#btn-connect').val('Connect');
    console.log('onConnectionLost');
}
