from backend import BaseHandler


class MainHandler(BaseHandler):

    def get(self):
        self.response.write('Agrihack API')
