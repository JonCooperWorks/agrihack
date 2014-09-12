import webapp2

import handlers
import config


routes = [
    ('/import/', handlers.ImportHandler),
    handlers.SMSHandler.mapping(),
]


app = webapp2.WSGIApplication(
    routes,
    debug=config.DEBUG)
