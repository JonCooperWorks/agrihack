from collections import Counter
import logging

from backend import send_sms
from backend.models import Farmer, Node


def handle(sms_message):
    message_body = sms_message.body
    if sms_message.to == 'demo@node-420.appspotmail.com':
        logging.info('Message received')
        return

    elif sms_message.to == 'whoami@node-420.appspotmail.com':
        logging.info('Message received from: ' + sms_message.sender)
        return reply_farmer_id(sms_message.sender)

    elif sms_message.to == 'status@node-420.appspotmail.com':
        farmer_id, node_id = message_body.split(' ')[1:]
        node = Node.get_by_node_id(node_id)
        if node is None:
            logging.error('Node not found')
            return send_sms(
                sms_message.sender,
                'You don\'t have any %s' % node_id
            )

        logging.info('Node found')
        return reply_node_status(sms_message.sender, node)


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
        message,
        sender='whoami@node-420.appspotmail.com',
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

    send_sms(farmer_id, message)

    logging.info(message)
