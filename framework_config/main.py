from framework_config.handlers import params_handlers

class PageNotFound404:
    def __call__(self, request):
        return '404 NOT FOUND', '404 Page Not Found'


class Framework:
    def __init__(self, urls, controllers):
        self.urls = urls
        self.controllers = controllers

    def __call__(self, environ, start_response):
        request = {}

        path = environ['PATH_INFO']
        if not path.endswith('/'):
            path = f'{path}/'

        method = environ['REQUEST_METHOD']
        request['method'] = method

        request['params'] = params_handlers[method]().get_params(environ)

        if path in self.urls:
            view = self.urls[path]
        else:
            view = PageNotFound404()

        for controller in self.controllers:
            controller(request)

        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
