import sys
import SocketServer
import BaseHTTPServer
import SimpleHTTPServer
import Queue


# Make it multithreaded 
class ThreadedHTTPD(SocketServer.ThreadingMixIn,BaseHTTPServer.HTTPServer):
    pass


# Override class to disable logging
class RequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    reqs = Queue.Queue()

    def do_POST(self):
	length = int(self.headers.getheader('content-length'))
	rdata = self.rfile.read(length)
	self.send_response(200, "OK")
	self.finish()
	#process_data(data, self.client_address)
	#print 'from %s: %s' % (self.client_address, data)
        RequestHandler.reqs.put(rdata)


    def log_message( self, format, *args ):
        """
        format: "%s" %s %s
        args: ('GET / HTTP/1.1', '200', '-')
        """
        if args[1] == '200':
	    if args[0].startswith('GET'):
		print 'path:', args[0].split(' ')[1]
	if args[0].startswith('POST'):
	    print args[0], args[2]


def start_new_httpd(dport):
    port = dport
    server_address = ('0.0.0.0', port)

    print 'HTTPD listens on %s:%d' % server_address
    httpd = ThreadedHTTPD(server_address, RequestHandler)
    while True: httpd.handle_request()


def main():
    port = [ int(sys.argv[1]) if sys.argv[1:] else 7788 ][0]
    import thread
    thread.start_new_thread(start_new_httpd, (port,))
    try:
        while True: pass
    except KeyboardInterrupt:
        print "HTTPD stoped."


if __name__ == '__main__':
    main()
