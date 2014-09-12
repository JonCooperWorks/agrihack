import os

from google.appengine.api import memcache
from google.appengine.api import mail
import webapp2
from webapp2_extras import jinja2


class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        # Configure i18n whenever we are using jinja2 to render a template.
        if self.get_current_profile():
            self.i18n.set_timezone(
                str(self.get_current_profile().get_timezone()))
        return jinja2.get_jinja2(app=self.app)

    def render_template(self, template, context=None):
        """Renders the template with the provided context (optional)."""
        context = context or {}

        extra_context = {
            'analytics': self.analytics,
            'csrf': self.csrf,
            'current_profile': self.get_current_profile(),
            'current_staff': self.get_current_staff(),
            'request': self.request,
            'session': self.session,
            'uri_for': self.uri_for}

        # Only override extra context stuff if it's not set by the template:
        for key, value in extra_context.items():
            if key not in context:
                context[key] = value

        return self.jinja2.render_template(template, **context)

    def render_to_response(self, template, context=None, use_cache=False):
        """Renders the template and writes the result to the response."""

        if use_cache:
            # Use the request's path to store the contents.

            # WARNING: This could cause scary problems if you render
            # user-specific pages.
            # DO NOT use current_profile in a template rendered with
            # use_cache=True.
            cache_key = self.request.path
            contents = memcache.get(cache_key)

            if not contents or 'flushcache' in self.request.arguments():
                contents = self.render_template(template, context)

                # If add() returns False, it means another request is already
                # trying to cache the page. No need to do anything here.
                if memcache.add('lock.%s' % cache_key, True):
                    memcache.set(cache_key, contents)
                    memcache.delete('lock.%s' % cache_key)

        else:
            contents = self.render_template(template, context)

        self.response.write(contents)

    def is_cron_request(self):
        return self.request.headers.get('X-Appengine-Cron') == 'true'

    def is_taskqueue_request(self):
        return 'X-AppEngine-QueueName' in self.request.headers

    def is_devappserver_request(self):
        return os.environ.get('APPLICATION_ID', '').startswith('dev~')


def send_sms(phone_number, body):
    return mail.send_mail(
        sender='alerts@420-node.appspot.com',
        to='%s@digitextjm.com' % phone_number,
        subject='',
        body=body)
