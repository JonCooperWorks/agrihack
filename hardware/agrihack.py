import serial, requests, json, time
from random import randrange

ser = serial.Serial('/dev/ttyACM0', 9600)
agrihack_url = 'http://node-420.appspot.com/datapoint/'
node_id = 'tomatoes'

while True:

  light_data = ser.readline()
  data = json.dumps({'node_id': str(node_id),
                    'temperature': str(randrange(50, 112)),
                    'pressure': str(randrange(0, 111)),
                    'humidity': str(randrange(0, 100)),
                    'light': str(light_data),
                    'saturation': str(randrange(0, 100))})

  requests.post(agrihack_url, data)
  print "data sent"
  time.sleep(2)

