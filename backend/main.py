import handlers

import webapp2


routes = [
    ('/api/', handlers.MainHandler),
]


app = webapp2.WSGIApplication(
    routes,
    debug=True)
