#! /usr/bin/env python3

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
        self._bus.write_i2c_block_data(
            self._addr,
            self._register['CTRL_REG1'],
            [0x7f])

    def is_connected(self):
        res = self._bus.read_byte_data(self._addr, self._register['WHO_AM_I'])
        if res == 0x33:
            return True
        else:
            return False

    def get_register_address(self, reg_name):
        if reg_name in self._register:
            return self._register[reg_name]
        else:
            return 0xFF