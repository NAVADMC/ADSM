import sys
import os
import signal
import shutil
import subprocess

from django.core.management.base import BaseCommand
from django.core.servers.basehttp import get_internal_wsgi_application
from django.conf import settings
from optparse import make_option
from tempfile import mkstemp
from time import sleep

import cherrypy


class Command(BaseCommand):
    help = r"""Run the Django project using CherryPy as the App Server and don't serve static files.

    CherryPy (http://www.cherrypy.org) is required.
    Futures (https://pypi.python.org/pypi/futures) is required (for CherryPy).

    Examples:
        Run a server with Django running on internal port 25566
            $ manage.py runproductionserver --host=0.0.0.0  --app_port=25566
    """
    args = "[--option=value, use `runproductionserver help` for help]"

    options = None
    PRODUCTIONSERVER_DIR = os.path.dirname(os.path.abspath(__file__))

    option_list = BaseCommand.option_list + (
        make_option('--host',
                    action='store',
                    type='string',
                    dest='host',
                    default='127.0.0.1',
                    help='Adapter to listen on. Default is 127.0.0.1'),
        make_option('--app_port',
                    action='store',
                    type='int',
                    dest='app_port',
                    default=8081,
                    help='Port for the CherryPy App Server (what hosts the Django App) to listen on. Default is 8181. Note, this must be different from the normal Server Port.')
    )

    def handle(self, *args, **options):
        self.options = options

        # Get this Django Project's WSGI Application and mount it
        application = get_internal_wsgi_application()
        cherrypy.tree.graft(application, "/")

        # Unsubscribe the default server
        cherrypy.server.unsubscribe()

        # Instantiate a new server
        server = cherrypy._cpserver.Server()

        # Configure the server
        server.socket_host = self.options['host']
        server.socket_port = self.options['app_port']
        server.thread_pool = 30

        server.max_request_body_size = 10737412742

        # For SSL Support
        # server.ssl_module = 'pyopenssl'
        # server.ssl_certificate = 'ssl/certificate.crt'
        # server.ssl_private_key = 'ssl/private.key'
        # server.ssl_certificate_chain = 'ssl/bundle.crt

        # Subscribe the new server
        server.subscribe()

        cherrypy.engine.start()
        #cherrypy.engine.block()  # I would like to use this as it listens to other CherryPy bad states. However, it causes the application to not catch the system close call correctly

        try:
            while(True):
                sleep(.1)
        except (KeyboardInterrupt, IOError, SystemExit) as e:
            try:
                print("Attempting to shutdown the server...")
                cherrypy.engine.exit()  # Need to call this first since we aren't blocking above
                print("Server shutdown.")
            except:
                print("Failed to shutdown server! Please press 'Ctrl+c.'")