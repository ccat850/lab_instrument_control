import usbtmc
import time as time 

# install: libusb , pyusb and ustmc ( python module) 

"""
[189924.313873] usb 1-1: new high-speed USB device number 4 using xhci_hcd
[189924.462597] usb 1-1: New USB device found, idVendor=0957, idProduct=1309, bcdDevice= 1.00
[189924.462602] usb 1-1: New USB device strings: Mfr=1, Product=2, SerialNumber=3
[189924.462604] usb 1-1: Product: E5061B
[189924.462605] usb 1-1: Manufacturer: Agilent Technologies
[189924.462607] usb 1-1: SerialNumber: MY49407492
[189924.484096] usbcore: registered new interface driver usbtmc
"""

idVendor='0957'
idProduct='1309'

sa = usbtmc.Instrument(int(idVendor, 16),int(idProduct, 16))

def get_id():
    sa.write("*IDN?")
    return sa.read()

def set_start_frequency(value):
    msg = f':SENS:FREQ:STAR {value}'
    sa.write(msg)

def set_ifbw(value):
    msg = f':SENS:BAND {value}'
    sa.write(msg)

def set_power(value):
    msg = f':SOUR1:POW {value}'
    sa.write(msg)

def set_stop_frequency(value):
    msg = f':SENS:FREQ:STOP {value}'
    sa.write(msg)

def save_s2p(fname):
    sa.write('DISP:WIND1:ACT')
    sa.write(":CALC:PAR:COUN 4")
    sa.write(':CALC1:PAR1:DEF S11')
    sa.write(':CALC1:PAR2:DEF S21')
    sa.write(':CALC1:PAR3:DEF S12')
    sa.write(':CALC1:PAR4:DEF S22')
    sa.write('MMEM:STOR:SNP:FORM RI')
    sa.write('MMEM:STOR:SNP:TYPE:S2P 1,2')
    sa.write(f'MMEM:STOR:SNP "{fname}"')
    sa.write(f'MMEM:TRAN? "{fname}"')
    s2pString = sa.read()
    with open(fname, 'w') as f:
        f.write(s2pString)
    sa.write(f'MMEM:DEL "{fname}"')

def get_frequency(units="GHz"):
    """Get CW frequency in given units.
    Args:
        units (str): frequency units
    Returns:
        str: frequency in selected units
    """

    msg = ':SENS1:FREQ:CENT?'
    sa.write(msg)
    return float(sa.read())

sa.close()
