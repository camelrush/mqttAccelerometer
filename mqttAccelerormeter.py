from devices.accelerometer import AccelerometerMPU6050 as MPU6050
import paho.mqtt.client
import ssl
import asyncio
import json
import time
import datetime

# Mqtt Define
AWSIoT_ENDPOINT = "a3ufrbqbd4cwta-ats.iot.ap-northeast-1.amazonaws.com"
MQTT_PORT = 8883
MQTT_TOPIC_PUB = "mqttAccelerometer"
MQTT_ROOTCA = "./awscert/AmazonRootCA1.pem"
MQTT_CERT = "./awscert/7bcb172755-certificate.pem.crt"
MQTT_PRIKEY = "./awscert/7bcb172755-private.pem.key"

def mqtt_connect(client, userdata, flags, respons_code):
    print('mqtt connected.') 
    # Entry Mqtt Subscribe.
    client.subscribe(MQTT_TOPIC_SUB)
    print('subscribe topic : ' + MQTT_TOPIC_SUB) 
 
def mqtt_message(client, userdata, msg):
    # Get Received Json Data 
    json_dict = json.loads(msg.payload)
    # if use ... json_dict['xxx']
    
# Publish Loop
async def pub_loop():
    acmeter = MPU6050()
    while True:
        # get Sensor data
        temp = acmeter.get_temp()
        ax, ay, az = acmeter.get_accel()
        gx, gy, gz = acmeter.get_gyro()
        tm = datetime.datetime.now()
        
        print('ax:{0:> .6f} ,ay:{1:> .6f} ,az:{2:> .6f}'.format(ax,ay,az))
        json_msg = json.dumps({"dt":tm.strftime('%Y-%m-%d %H:%M:%S.%f'),"ax":ax,"ay":ay,"az":az,"gx":gx,"gy":gy,"gz":gz,"temp":temp})

        # mqtt Publish
        client.publish(MQTT_TOPIC_PUB ,json_msg)
        time.sleep(0.01)

# Main Procedure
if __name__ == '__main__':
    # Mqtt Client Initialize
    client = paho.mqtt.client.Client()
    client.on_connect = mqtt_connect
    client.on_message = mqtt_message
    client.tls_set(MQTT_ROOTCA, certfile=MQTT_CERT, keyfile=MQTT_PRIKEY, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

    # Connect To Mqtt Broker(aws)
    client.connect(AWSIoT_ENDPOINT, port=MQTT_PORT, keepalive=60)

    # Start Mqtt Subscribe 
    client.loop_start()

    # Start Publish Loop 
    loop = asyncio.get_event_loop()
    loop.run_until_complete(pub_loop())
