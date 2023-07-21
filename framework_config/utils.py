from quopri import decodestring


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
