class PageNotFound404:
    def __call__(self, request):
        return '404 NOT FOUND', '404 Page Not Found'


class Framework:
    def __init__(self, urls, controllers):
        self.urls = urls
        self.controllers = controllers

    def __call__(self, request, response):
        path = request['PATH_INFO']

        if not path.endswith('/'):
            path = f'{path}/'

        if path in self.urls:
            view = self.urls[path]
        else:
            view = PageNotFound404()
        context = {}

        for front in self.controllers:
            front(context)

        code, body = view(context)
        response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
