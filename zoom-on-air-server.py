#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import RPi.GPIO as GPIO

status = "OFF"

class S(BaseHTTPRequestHandler):

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        global status
        self._set_response()
        self.wfile.write(status.format(self.path).encode('utf-8'))

    def do_POST(self):
        global status
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        status = post_data.decode('utf-8')
        logging.info("Status: "+status)

        if status == "ON":
            GPIO.output(18,GPIO.HIGH)
        else:
            GPIO.output(18,GPIO.LOW)
        self._set_response()
        self.wfile.write("OK".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8080):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(18,GPIO.OUT)
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
