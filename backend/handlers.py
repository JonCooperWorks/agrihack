import datetime
import json
import logging
import random
import re
import string

from google.appengine.ext import ndb
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler

from backend import BaseHandler
from models import Farmer, SMSMessage


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
                dob=datetime.datetime.now() - datetime.timedelta(days=20*365),
                address='Computer Science Postgrab Lab',
                alias=generate_alias(first_name, last_name),
                farmer_idx=random.randint(1, 100000),
                parish='UWI',
                main_activity='Farming',
            ))

        ndb.put_multi(farmers)
        return self.json_response({'status': 'done'})


class SMSHandler(InboundMailHandler):
    """Handles inbound SMS messages from farmers."""

    def receive(self, mail_message):
        for message in mail_message.bodies('text/html'):
            _, body = message
            sender, = re.findall(
                r'([0-9]{11})@mms.digicelgroup.com',
                mail_message.sender)
            sms_message = SMSMessage(body=body.decode(), sender=sender)
            sms_message.put()
            logging.info('Stored message from %s' % sender)


class NodeDataHandler(BaseHandler):
    """Handles inbound data from a Node 420 in the field.

    The field Node 420 sends data points in POST requests to this handler,
    that are persisted to the Datastore."""

    def post(self):
        sensor_data = json.loads(self.request.body)
        DataPoint(**sensor_data).put()
        return self.json_response({'status': 'success'})


def generate_farmer_id():
    char_set = string.ascii_uppercase + string.digits
    return ''.join(random.sample(char_set, 10))


def generate_alias(first_name, last_name):
    return first_name[0] + last_name[0] + 'izzle'
