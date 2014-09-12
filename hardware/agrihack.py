import serial, requests, json
from random import randrange

ser = serial.Serial('/dev/tty.usbserial', 9600)
agrihack_url = 'http://node-420.appspot.com'
node_id = 000001

while True:

  light_data = ser.readline()
  data = json.dumps('node_id': randrange(10000, 99999),
                    'temperature': randrang(50, 112),
                    'pressure': randrange(0, 111),
                    'humidity': randrange(0, 100),
                    'light': light,
                    'saturation': randrange(0, 100))

  requests.post(agrihack_url, data)
  
