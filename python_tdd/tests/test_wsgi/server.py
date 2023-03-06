'''
Small wsgiref based web server.
Takes a path to serve from and an optional port number (defaults to 8000),
then tries to serve files.
MIME types are guessed from the file names,
404 errors are raised if the file is not found.
'''
import mimetypes
import os
import sys
import wsgiref.simple_server
import wsgiref.util

def get_mime_type(filename):
    return mimetypes.guess_type(filename)[0]

def get_filename(environ):
    filename = os.path.join(path, environ["PATH_INFO"][1:])
    if "." not in filename.split(os.path.sep)[-1]:
        filename = os.path.join(filename, "index.html")
    return filename

def get_path(args):
    if len(args) > 1:
        return args[1]
    else:
        return os.getcwd()

def get_port(args):
    if len(args) > 2:
        return int(args[2])
    else:
        return 8000

def app(environ, respond):
    filename = get_filename(environ)

    if os.path.exists(filename):
        respond("200 OK", [("Content-Type", get_mime_type(filename))])
        return wsgiref.util.FileWrapper(open(filename, "rb"))
    else:
        respond("404 Not Found", [("Content-Type", "text/plain")])
        return [b"not found"]


if __name__ == "__main__":
    path = get_path(sys.argv)
    port = get_port(sys.argv)

    with wsgiref.simple_server.make_server('', port, app) as httpd:
        print(f"Serving {path} on port {port}, control-C to stop")
        httpd.serve_forever()