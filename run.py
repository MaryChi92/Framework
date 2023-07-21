from wsgiref.simple_server import make_server
from whitenoise import WhiteNoise

from framework_config.main import Framework
from mainapp.urls import urls, fronts


app = Framework(urls, fronts)
app = WhiteNoise(app)
app.add_files('./static', 'static/')


if __name__ == "__main__":
    server = make_server('', 8080, app)
    print("Server running on port 8080")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Keyboard Interrupt')
