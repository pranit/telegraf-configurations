from pyA20.gpio import gpio
from pyA20.gpio import port
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS, WritePrecision
import dht
import time
from datetime import datetime

# InfluxDB v2 credentials and settings
INFLUXDB_URL = "http://IP_ADDR:8086"
INFLUXDB_TOKEN = "TOKEN"
INFLUXDB_ORG = "ORG"
INFLUXDB_BUCKET = "BUCKET"

# initialize GPIO
PIN2 = port.PA6
gpio.init()

# InfluxDB v2 client
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

# read data using pin
instance = dht.DHT(pin=PIN2)
while True:
    result = instance.read()
    if result.is_valid():
            print("Last valid input: " + str(datetime.now()))
            print("Temperature: {0:0.1f} C".format(result.temperature))
            print("Humidity: {0:0.1f} %".format(result.humidity))

    # Write data to InfluxDB v2
            point = Point("sensor_data") \
                .tag("location", "OutdoorEastFacing") \
                .field("temperature", result.temperature) \
                .field("humidity", result.humidity) \
                .time(datetime.utcnow(), WritePrecision.NS)
            write_api.write(INFLUXDB_BUCKET, INFLUXDB_ORG, point)
    time.sleep(15)

