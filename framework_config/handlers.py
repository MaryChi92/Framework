from framework_config.utils import parse_request_params, decode_values


class GetMethodHandler:
    @staticmethod
    def get_params(env):
        query_string = env["QUERY_STRING"]
        return parse_request_params(query_string)


class PostMethodHandler:
    @staticmethod
    def get_request_params(env):
        try:
            content_length = int(env.get("CONTENT_LENGTH"))
        except TypeError:
            content_length = 0

        data = env["wsgi.input"].read(content_length) if content_length > 0 else b""
        return data

    @staticmethod
    def parse_data(data):
        result = {}
        if data:
            data_str = data.decode("utf-8")
            result = decode_values(parse_request_params(data_str))
        return result

    def get_params(self, environ):
        data = self.get_request_params(environ)
        result = self.parse_data(data)
        return result


params_handlers = {
    "GET": GetMethodHandler,
    "POST": PostMethodHandler,
}
