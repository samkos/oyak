#!/usr/bin/env python
 
import BaseHTTPServer
import CGIHTTPServer
 
server = BaseHTTPServer.HTTPServer
handler = CGIHTTPServer.CGIHTTPRequestHandler
server_address = ("", 7777)
handler.cgi_directories = ["/home/samy/GIT/OYAK/device/appli/"]
 
httpd = server(server_address, handler)
httpd.serve_forever()
