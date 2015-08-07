from keystone.server import wsgi

application = wsgi.initialize_application('admin')
