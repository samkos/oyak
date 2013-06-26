#!/usr/bin/env python
 
import BaseHTTPServer
import CGIHTTPServer
 
server = BaseHTTPServer.HTTPServer
handler = CGIHTTPServer.CGIHTTPRequestHandler
server_address = ("", 7777)
#handler.cgi_directories = ["/home/samy/GIT/OYAK/device/appli/"]
 
handler.cgi_directories = ["/cgi-bin"]
 
httpd = server(server_address, handler)
httpd.serve_forever()
