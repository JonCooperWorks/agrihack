from collections import Counter
import logging

from backend import send_sms
from backend.models import Farmer, Node


def handle(sms_message):
    command_name, farmer_id, node_id = sms_message.body.split(' ')
    command = COMMANDS[command_name.lower()]
    node = Node.get_by_node_id(node_id)
    if node is None:
        logging.error('Node not found')
        return send_sms(
            sms_message.sender,
            'You don\'t have any %s' % node_id
        )

    logging.info('Node found')
    return command(farmer_id, node)


def get_node_status(farmer_id, node):
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


COMMANDS = {
    'status': get_node_status
}
