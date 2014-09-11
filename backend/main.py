import webapp2

import handlers
import config


routes = [
    ('/api/', handlers.MainHandler),
]


app = webapp2.WSGIApplication(
    routes,
    debug=config.DEBUG)
