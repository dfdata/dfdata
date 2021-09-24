import sys
import os
import mimetypes
from wsgiref import simple_server, util

path = os.path.join(os.getcwd(), 'build/html')
#print(path)

def app(environ, respond):

    fn = os.path.join(path, environ['PATH_INFO'][1:])
    if '.' not in fn.split(os.path.sep)[-1]:
        fn = os.path.join(fn, 'index.html')
    type = mimetypes.guess_type(fn)[0]

    if os.path.exists(fn):
        respond('200 OK', [('Content-Type', type)])
        return util.FileWrapper(open(fn, "rb"))
    else:
        respond('404 Not Found', [('Content-Type', 'text/plain')])
        return [b'404 Not Found']

#启动服务器，传入函数app
httpd = simple_server.make_server('', 8082, app)
print("Serving HTTP on port 8082...")
httpd.serve_forever()
