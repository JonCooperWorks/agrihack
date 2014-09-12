import webapp2

import handlers
import config


routes = [
    ('/api/', handlers.MainHandler),
    handlers.SMSHandler.mapping(),
]


app = webapp2.WSGIApplication(
    routes,
    debug=config.DEBUG)
