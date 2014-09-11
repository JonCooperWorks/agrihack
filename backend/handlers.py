import logging
import re

from google.appengine.ext.webapp.mail_handlers import InboundMailHandler

from backend import BaseHandler
from models import SMSMessage


class MainHandler(BaseHandler):

    def get(self):
        self.response.write('Agrihack API')


class SMSHandler(InboundMailHandler):
    """Handles inbound SMS messages from farmers."""

    def receive(self, mail_message):
        for message in mail_message.bodies('text/html'):
            _, body = message
            # Parse phone number from <phone-number>@mms.digicelgroup.com
            sender, = re.findall(
                r'([0-9]{11})@mms.digicelgroup.com',
                mail_message.sender)
            sms_message = SMSMessage(body=body.decode(), sender=sender)
            sms_message.put()
            logging.info('Stored message from %s' % sender)
