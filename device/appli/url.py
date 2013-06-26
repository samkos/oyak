#!/usr/bin/env python
 
import cgi
 
form = cgi.FieldStorage()
 
val1 = form.getvalue('first')
val2 = form.getvalue('last')
 
print """Content-type: text/html
 
<html><head><title>Test URL Encoding</title></head><body>
Hello my name is %s %s
</body></html>""" % (val1, val2)
