import sys
import SocketServer
import BaseHTTPServer
import SimpleHTTPServer

# Make it multithreaded 
class ThreadedHTTPD(SocketServer.ThreadingMixIn,BaseHTTPServer.HTTPServer):
    pass

# Override class to disable logging
class RequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def log_message( self, format, *args ):
        """
        format: "%s" %s %s
        args: ('GET / HTTP/1.1', '200', '-')
        """
        print args[0].split(' ')[1]


port = [ int(sys.argv[1]) if sys.argv[1:] else 5422 ][0]
server_address = ('0.0.0.0', port)
print "Serving HTTP on", server_address

httpd = ThreadedHTTPD(server_address, RequestHandler)
try:
    while True:
        httpd.handle_request()
except KeyboardInterrupt:
    print "Finished"
