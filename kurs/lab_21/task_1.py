"""Write a simple wsgi compatible application that prints the username, remote address, user agent,
path and your surname(see below). Add a simple middleware that adds the key SURNAME with the value of your surname
to the environ.
Add another middleware that changes the formatting of all the symbols to be lowercase
(except of the first ones in sentence and your surname). Use two middlewares simultaneously.
"""
from webob import Response
from wsgiref.simple_server import make_server


HOST_NAME = "localhost"
PORT = 8001


class Middleware:
    def __init__(self, application, surname):
        self.app = application
        self.surname = surname

    def __call__(self, environ, start_response):
        environ = self.add_surname(environ)
        res = self.app(environ, start_response)
        return self.change_data(environ, res)

    def add_surname(self, environ):
        environ['SURNAME'] = self.surname
        return environ

    @staticmethod
    def change_data(environ, res):
        res = res[0].decode('utf-8')
        res = res.lower()
        temp = environ['SURNAME']
        res = res.replace(temp, f"{temp[0].upper()}{temp[1:]}")
        res = f"{res[0].upper()}{res[1:]}"
        return [res.encode('utf-8')]


class MyApp:
    def __call__(self, environ, start_response):
        response = Response()
        response.text = self.create_response(environ)
        return response(environ, start_response)

    @staticmethod
    def create_response(environ):
        return f"User_name: {environ['USERNAME']} {environ['SURNAME']}, address: {environ['REMOTE_ADDR']}," \
               f" agent: {environ['HTTP_USER_AGENT']}"


if __name__ == "__main__":
    input_text = input("Input you'r surname: ")
    with make_server(HOST_NAME, PORT, app=Middleware(MyApp(), input_text)) as server:
        print(f"Server started http://{HOST_NAME}:{PORT}")
        server.serve_forever()


