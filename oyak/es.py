
import barcode
from barcode.writer import ImageWriter
print barcode.PROVIDED_BARCODES
EAN = barcode.get_barcode_class('ean13')

ean = EAN(u'5901234123457', writer=ImageWriter())
fullname = ean.save('ean13_barcode')
f = open('test.png', 'wb')
ean.write(f) # PIL (ImageWriter) produces RAW format here
f.close()


