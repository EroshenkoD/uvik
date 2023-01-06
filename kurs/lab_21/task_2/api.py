from parse import parse
from webob import Response
from middleware import Middleware


class API:
    def __init__(self):
        self.routes = {}
        self.middleware = Middleware(self)

    def __call__(self, environ, start_response):
        return self.middleware(environ, start_response)

    def route(self, path):
        def wrapper(handler):
            self.routes[path] = handler
            return handler
        return wrapper

    @staticmethod
    def default_response(response):
        response.status_code = 404
        response.text = "Not found!"

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named
        return None, None

    def handle_request(self, request):
        response = Response()
        response.content_type = "application/json"
        handler, kwargs = self.find_handler(request_path=request.path)
        if handler is not None:
            handler(request, response, **kwargs)
        else:
            self.default_response(response)
        return response

    def add_middleware(self, middleware_cls):
        self.middleware.add(middleware_cls)
