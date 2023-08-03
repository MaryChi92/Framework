from quopri import decodestring
from time import time


def parse_request_params(params: str):
    data = {}
    if params:
        params = params.split('&')
        for param in params:
            k, v = param.split('=')
            data[k] = v
    return data


def decode_values(data):
    new_data = {}
    for k, v in data.items():
        new_v = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
        new_v_decode_str = decodestring(new_v).decode('UTF-8')
        new_data[k] = new_v_decode_str
    return new_data


class AppRoute:
    routes = {}

    def __init__(self, url):
        self.url = url

    def __call__(self, cls):
        self.routes[self.url] = cls()


def debug(func):
    def wrap(*args, **kwargs):
        time_before = time()
        func_name = func.__name__
        result = func(*args, **kwargs)
        time_after = time()
        time_delta = time_after - time_before
        print(f'debug: function {func_name}: {time_delta}')
        return result
    return wrap
