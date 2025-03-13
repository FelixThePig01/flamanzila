import subprocess
from wsgiref.simple_server import make_server
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.config import Configurator
from urllib.parse import urlparse

@view_config(route_name='index', renderer='form.html')
def index(request):
    return {}

@view_config(route_name='run', request_method='POST', renderer='success.html')
def run_command(request):
    name = request.params['name']
    tmux_session = "minecraft"  # Numele sesiunii tmux

    # Comanda care va fi trimisă în sesiunea tmux
    command = f"tmux send-keys -t {tmux_session} 'whitelist add {name}' C-m"
    subprocess.run(command, shell=True)

    # Obținem adresa IP a serverului din request (fără localhost)
    host = request.host.split(':')[0]  # Luați doar IP-ul fără port
    return redirect(f'http://fuxilandru.go.ro:5000/run_confirmation')


@view_config(route_name='run_confirmation', renderer='confirmation.html')
def run_confirmation(request):
    name = request.params.get('name', 'necunoscut')
    return {"message": f"L-am băgat pe {name} pe whitelist"}

if __name__ == '__main__':
    with Configurator() as config:
        config.include('pyramid_jinja2')
        config.add_jinja2_renderer(".html")
        config.add_route('index', '/')
        config.add_route('run', '/run')
        config.add_route('run_confirmation', '/run_confirmation')
        config.scan()
        app = config.make_wsgi_app()

    server = make_server('0.0.0.0', 5000, app)
    server.serve_forever()
