from collections import Counter
import logging

from backend import send_sms
from backend.models import Farmer, Node


def handle(sms_message):
    message_body = sms_message.body
    command_name = message_body.split(' ')[0]
    if command_name.lower() == 'status':
        farmer_id, node_id = message_body.split(' ')[1:]
        node = Node.get_by_node_id(node_id)
        if node is None:
            logging.error('Node not found')
            return send_sms(
                sms_message.sender,
                'You don\'t have any %s' % node_id
            )

        logging.info('Node found')
        return reply_node_status(farmer_id, node)
    elif command_name.lower() == 'whoami':
        return reply_farmer_id(sms_message.sender)


def reply_farmer_id(cell_number):
    farmer = Farmer.get_by_cell_number(cell_number)
    if farmer is None:
        logging.error('Farmer not found')
        return send_sms(
            cell_number,
            'Register with RADA to access this service.'
        )
    message = """
Hello, {farmer.first_name} {farmer.last_name}!
Your farmer ID is {farmer.farmer_id}.
""".format(farmer=farmer)
    send_sms(
        cell_number,
        message
    )
    logging.info(message)



def reply_node_status(farmer_id, node):
    """Responds to a message in the form

        STATUS <FARMER_ID> <NODE_ID>

    with the status of the area compared to optimal values for that crop.
    """
    data_points = node.data_points()
    temp_readings = Counter([data_point.temperature
                             for data_point in data_points])
    pressure_readings = Counter([data_point.temperature
                                 for data_point in data_points])
    humidity_readings = Counter([data_point.temperature
                                 for data_point in data_points])
    light_readings = Counter([data_point.temperature
                              for data_point in data_points])
    saturation_readings = Counter([data_point.temperature
                                   for data_point in data_points])

    sensor_summary = {
        'mode_temperature': temp_readings.most_common(1)[0][0],
        'mode_pressure': pressure_readings.most_common(1)[0][0],
        'mode_humidity': humidity_readings.most_common(1)[0][0],
        'mode_light': light_readings.most_common(1)[0][0],
        'mode_saturation': saturation_readings.most_common(1)[0][0],
    }

    message = """
Stats for {node_id}:

    Temperature: {mode_temperature} C
    Pressure: {mode_pressure} Bar
    Humidity: {mode_humidity}%
    Light: {mode_light}
    Saturation: {mode_saturation}
""".format(
        node_id=node.node_id,
        **sensor_summary
    )

    # Get averages and compare with guidelines for that crop then send SMS to
    # farmer.
    # Since this is a demo, we'll text everyone.
    for farmer in Farmer.query():
        send_sms(farmer.cell_number, message)

    logging.info(message)
