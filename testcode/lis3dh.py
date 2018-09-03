#! /usr/bin/env python3

import smbus2
from time import sleep
from datetime import datetime

'''
class lis3dh:
    def __init__(self, bus):
        self._bus = bus

    def read_lis3dh(self.h_reg, addr=0x18):
        h = bus.read_word_data(addr,  reg)
        l = bus.read_word_data(addr, reg+1)
        return h<<8 | l
'''

def s8(value):
    return -(value & 0b10000000) | (value & 0b01111111)

def read(bus):
    #status = bus.read_byte_data(0x18, 0x27)
    #if status != 1:
    #    return False
    plot = {}
    h = bus.read_byte_data(0x18, 0x28)
    l = bus.read_byte_data(0x18, 0x29)
    plot['x'] = s8(h<<8|l)
    h = bus.read_byte_data(0x18, 0x2a)
    l = bus.read_byte_data(0x18, 0x2b)
    plot['y'] = s8(h<<8|l)
    h = bus.read_byte_data(0x18, 0x2c)
    l = bus.read_byte_data(0x18, 0x2d)
    plot['z'] = s8(h<<8|l)
    return plot

def main(name):
    bus = smbus2.SMBus(1)
    bus.write_i2c_block_data(0x18,0x20,[0x7f])
    try:
        f = open(name, 'w')
        count = 0
        while True:
            data = read(bus)
            if count == 100:
                print(data)
                count = 0
            f.write(str(data['x'])+','+str(data['y'])+','+str(data['z'])+'\n')
            count += 1
            sleep(0.001)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
    finally:
        f.close()

if __name__ == '__main__':
    now = datetime.now()
    name = now.strftime('data/%Y%m%d_%H:%M:%S.csv')
    print(name)
    main(name)
