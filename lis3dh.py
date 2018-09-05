#! /usr/bin/env python3

#import numpy as np
from time import sleep

class RegisterNameError(Exception):
    def __init__(self, reg_name):
        self._name = reg_name
        self._message = 'No such register name: {0}'.format(self._name)

    def __str__(self):
        return self._message

class Lis3dh(object):
    def __init__(self, bus, addr=0x18):
        self._bus = bus
        self._addr = addr
        self._register = {
            'WHO_AM_I' : 0x0f,
            'X_L' : 0x28,
            'X_H' : 0x29,
            'Y_L' : 0x2a,
            'Y_H' : 0x2b,
            'Z_L' : 0x2c,
            'Z_H' : 0x2d,
            'CTRL_REG1' : 0x20
        }
        self._default_value = {
            'x' : 0.0,
            'y' : 0.0,
            'z' : 0.0
        }
        self._bus.write_i2c_block_data(
            self._addr,
            self._register['CTRL_REG1'],
            [0x7f])

    def read(self, reg_name):
        if reg_name not in self._register:
            raise RegisterNameError(reg_name)
        return self._bus.read_byte_data(
            self._addr,
            self._register[reg_name]
        )

    def is_connected(self):
        res = self.read('WHO_AM_I')
        if res == 0x33:
            return True
        else:
            return False

    def get_register_address(self, reg_name):
        if reg_name in self._register:
            return self._register[reg_name]
        else:
            raise RegisterNameError(reg_name)

    def get_acceleration(self):
        l = self.read('X_L')
        h = self.read('X_H')
        #x = (h << 8 | l) >> 4
        x = (l << 8 | h)
        x = self.byte2int(x) / 1024.0 * 980.0 - self._default_value['x']

        l = self.read('Y_L')
        h = self.read('Y_H')
        #y = (h << 8 | l) >> 4
        y = (l << 8 | h)
        y = self.byte2int(y) / 1024.0 * 980.0 - self._default_value['y']

        l = self.read('Z_L')
        h = self.read('Z_H')
        #z = (h << 8 | l) >> 4
        z = (l << 8 | l)
        z = self.byte2int(z) / 1024.0 * 980.0 - self._default_value['z']

        return (x, y,z)
    
    def calibration(self):
        data = [0.0, 0.0, 0.0]
        for i in range(1000):
            x,y,z = self.get_acceleration()
            data[0] += x
            data[1] += y
            data[2] += z
            sleep(0.001)
        for i in range(3):
            data[i] = data[i] / 1000
        self._default_value['x'] = data[0]
        self._default_value['y'] = data[1] 
        self._default_value['z'] = data[2]

    def byte2int(self, value):
        #return -(value & 0b100000000000) | (value & 0b011111111111)
        return -(value & 0b10000000) | (value & 0b01111111)

def main():
    print('Hello, world!')
    try:
        raise RegisterNameError('WHO_AM_I')
    finally:
        print('Hello, world!')

if __name__ == '__main__':
    main()