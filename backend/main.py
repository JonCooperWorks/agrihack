import webapp2

import handlers


routes = [
    ('/import/', handlers.ImportHandler),
    ('/datapoint/', handlers.DataPointHandler),
    handlers.SMSHandler.mapping(),
]


app = webapp2.WSGIApplication(
    routes,
    debug=True)
