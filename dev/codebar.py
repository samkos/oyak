from reportlab.graphics.barcode import code39, code128
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm,inch
from reportlab.pdfgen import canvas
import os, sys

c = canvas.Canvas("barcode_example.pdf", pagesize=A4)

code_list = [
    '123456789', '987654321', '349871637', '291874653', '123451234',
    '897645362', '761239403', '891237456', '712398476', '290483721',
    '123456789', '987654321', '349871637', '291874653', '123451234',
    '897645362', '761239403', '891237456', '712398476', '290483721',
    '123456789', '987654321', '349871637', '291874653', '123451234',
    '897645362', '761239403', '891237456', '712398476', '290483721',
    '123456789', '987654321', '349871637', '291874653', '123451234',
    '897645362', '761239403', '891237456', '712398476', '290483721',
    '123456789', '987654321', '349871637', '291874653', '123451234',
    '897645362', '761239403', '891237456', '712398476', '290483721',
    '123456789', '987654321', '349871637', '291874653', '123451234',
    '897645362', '761239403', '891237456', '712398476', '290483721',
    '123456789', '987654321', '349871637', '291874653', '123451234',
    '897645362', '761239403', '891237456', '712398476', '290483721']

x = 1 * mm
y = 285 * mm - inch
x1 = 6.4 * mm

print mm

for code in code_list:
    barcode = code128.Code128(code,barWidth = 0.015 * inch, barHeight = 1. * inch, fontSize = 30, humanReadable = True)
    barcode.drawOn(c, x, y)
    x = x
    y = y - 1.8 * inch

    if int(y) <= 0:
        x = x + 140 * mm
        y = 285 * mm - inch

c.showPage()
c.save()


if sys.platform.startswith("linux"):
  os.system("evince barcode_example.pdf")
