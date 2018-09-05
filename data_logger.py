#! /usr/bin/env python3

from smbus2 import SMBus
from lis3dh import Lis3dh
from datetime import datetime
from time import sleep
import csv

def main():
    bus = SMBus(1)
    sensor = Lis3dh(bus)
    filename = datetime.now().strftime('logdata/%Y%M%d_%H%m%s.csv') 
    f = open(filename, 'w')
    writer = csv.writer(f, lineterminator='\n')
    try:
        run(sensor, writer)
    except KeyboardInterrupt:
        pass
    finally:
        f.close()

    
def run(sensor, file):
    count = 0
    while True:
        datalist = sensor.get_acceleration()
        file.writerow(datalist)
        if count == 1000:
            print(datalist)
            count = 0
        else:
            count += 1
        sleep(0.001)

if __name__ == '__main__':
    main()