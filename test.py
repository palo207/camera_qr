from datetime import datetime
from config import path_write,separator
from operator import itemgetter

# Zapis barcodov do súboru
def write_data_into_file(barcodes_in_order):
    w_file = open(path_write,'a+')
    w_file.truncate(0)
    w_file.write(separator.join(barcodes_in_order))
    w_file.close()
    return 0
barcodes_in_order=[]
barcodes_in_order.append([100,10,'barcode1'])


barcodes_in_order = sorted(barcodes_in_order, key=itemgetter(0))
if barcodes_in_order:
    barcodes_in_order = [x[2] for x in barcodes_in_order]
    write_time = str(datetime.now())
    barcodes_in_order.insert(0,write_time)
    write_data_into_file(barcodes_in_order)


