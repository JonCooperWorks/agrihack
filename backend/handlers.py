import datetime
import json
import logging
import random
import re
import string

from google.appengine.ext import ndb
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler

from backend import BaseHandler, sms_commands
from models import DataPoint, Farmer, Node, SMSMessage


class ImportHandler(BaseHandler):

    def get(self):
        # If we've already imported farmers, don't bother to import them from
        # the JSON file.
        if Farmer.query().count() > 0:
            return self.json_response({'status': 'already_populated'})

        with open('attendees.json') as attendees_file:
            attendees = json.loads(attendees_file.read())

        farmers = []
        for name, cell_number in attendees.iteritems():
            first_name, last_name = name.split(' ')
            farmers.append(Farmer(
                first_name=first_name,
                last_name=last_name,
                cell_number=cell_number,
                house_number=cell_number,
                farmer_id=generate_farmer_id(),
                verified=True,
                dob=datetime.datetime.now() -
                datetime.timedelta(days=20 * 365),
                address='Computer Science Postgrab Lab',
                alias=generate_alias(first_name, last_name),
                farmer_idx=random.randint(1, 100000),
                parish='UWI',
                main_activity='Farming',
            ))

        node = Node(node_id='00420')
        ndb.put_multi(farmers + [node])

        for _ in range(50):
            DataPoint(
                temperature=random.randint(40, 90),
                pressure=random.randint(20, 30),
                humidity=random.randint(65, 100),
                light=random.randint(0, 100),
                saturation=random.randint(30, 90),
                parent=node.key,
            ).put()

        return self.json_response({'status': 'done'})


class SMSHandler(InboundMailHandler):

    """Handles inbound SMS messages from farmers."""

    def receive(self, mail_message):
        if mail_message.to == 'demo@node-420.appspot.com':
            logging.info('Message received')
            return

        for message in mail_message.bodies('text/html'):
            _, body = message
            sender, = re.findall(
                r'([0-9]{11})@mms.digicelgroup.com',
                mail_message.sender)
            sms_message = SMSMessage(body=body.decode(), sender=sender)
            sms_message.put()
            sms_commands.handle(sms_message)
            logging.info('Stored message from %s' % sender)


class DataPointHandler(BaseHandler):

    """Handles inbound data from a Node 420 in the field.

    The field Node 420 sends data points in POST requests to this handler,
    that are persisted to the Datastore."""

    def post(self):
        sensor_data = json.loads(self.request.body)
        node = Node.get_by_node_id(sensor_data['node_id'])
        if not node:
            return self.abort(404)

        del sensor_data['node_id']
        DataPoint(parent=node.key, **sensor_data).put()
        self.response.status_code = 201
        return self.json_response({'status': 'success'})


def generate_farmer_id():
    char_set = string.ascii_uppercase + string.digits
    return ''.join(random.sample(char_set, 10))


def generate_alias(first_name, last_name):
    return first_name[0] + last_name[0] + 'izzle'
