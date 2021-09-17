from datetime import datetime
from config import path_write,separator

# Zapis barcodov do súboru
def write_data_into_file(barcodes_in_order):
    w_file = open(path_write,'a+')
    w_file.truncate(0)
    w_file.write(separator.join(barcodes_in_order))
    w_file.close()
    return 0

write_time = str(datetime.now())
barcode_data = ['barcode1','barcode181']
barcode_data.insert(0,write_time)
write_data_into_file(barcode_data)