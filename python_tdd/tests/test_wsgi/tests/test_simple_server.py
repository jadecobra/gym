import wsgiref.simple_server

with wsgiref.simple_server.make_server('', 8000, wsgiref.simple_server.demo_app) as httpd:
    print('Serving HTTP on port 8000...')

    # Respond to requests until process is killed
    # httpd.serve_forever()

    # Alternative: serve one request, then exit
    httpd.handle_request()