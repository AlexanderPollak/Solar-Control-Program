#!/usr/bin/env python
# -*- coding: utf-8 -*-

# read_register
# read 10 registers and print result on stdout

# you can use the tiny modbus server "mbserverd" to test this code
# mbserverd is here: https://github.com/sourceperl/mbserverd

# the command line modbus client mbtget can also be useful
# mbtget is here: https://github.com/sourceperl/mbtget

from pyModbusTCP.client import ModbusClient
from pymodbus.payload import BinaryPayloadDecoder, BinaryPayloadBuilder
import time


def encode_field(self, value, mb_type='unit16'):
    builder = BinaryPayloadBuilder(endian=self.endian)
    if mb_type == 'bit' or mb_type == 'bits':
        builder.add_bits(value)
    elif mb_type == 'uint8':
        builder.add_8bit_uint(value)
    elif mb_type == 'uint16':
        builder.add_16bit_uint(value)
    elif mb_type == 'uint32':
        builder.add_32bit_uint(value)
    elif mb_type == 'uint64':
        builder.add_64bit_uint(value)
    elif mb_type == 'int8':
        builder.add_8bit_int(value)
    elif mb_type == 'int16':
        builder.add_16bit_int(value)
    elif mb_type == 'int32':
        builder.add_32bit_int(value)
    elif mb_type == 'int64':
        builder.add_64bit_int(value)
    elif mb_type == 'float32':
        builder.add_32bit_float(value)
    elif mb_type == 'float64':
        builder.add_64bit_float(value)
    elif mb_type == 'string' or mb_type == 'str':
        builder.add_string(value)
    else:
        print('Not supported DataType: "%s"' % mb_type)
    return builder.build()


def decode(self, raw, size, mb_type, mb_funcall=3):
    print('decode param (raw=%s, size=%s, mb_type=%s, mb_funcall=%s)' % (raw, size, mb_type, mb_funcall))
    if mb_funcall == 1:
        # Read Coil Status (FC=01)
        print("decoder FC1 (raw: %s)" % raw)
        decoder = BinaryPayloadDecoder.fromCoils(raw, endian=self.endian)
    elif mb_funcall == 2:
        # Read Discrete Input (FC=02)
        print("decoder FC2 (raw: %s)" % raw)
        decoder = BinaryPayloadDecoder(raw, endian=self.endian)
    elif mb_funcall == 3:
        # Read Holding Registers (FC=03)
        print("decoder FC3 (raw: %s)" % raw)
        decoder = BinaryPayloadDecoder.fromRegisters(raw, endian=self.endian)
    elif mb_funcall == 4:
        # Read Input Registers (FC=04)
        print("decoder stub FC4 (raw: %s)" % raw)
        decoder = BinaryPayloadDecoder(raw, endian=self.endian)
    else:
        print("Function call not supported: %s" % mb_funcall)
        decoder = None

    result = ""
    if mb_type == 'bitmap':
        if size == 1:
            mb_type = 'int8'
        elif size == 2:
            mb_type = 'int16'
        elif size == 2:
            mb_type = 'int32'
        elif size == 4:
            mb_type = 'int64'

    if decoder is None:
        print("decode none")
        result = raw
    else:
        try:
            if mb_type == 'string' or mb_type == 'utf8':
                result = decoder.decode_string(size)
            # elif mb_type == 'bitmap':
            #	result = decoder.decode_string(size)
            elif mb_type == 'datetime':
                result = decoder.decode_string(size)
            elif mb_type == 'uint8':
                result = int(decoder.decode_8bit_uint())
            elif mb_type == 'int8':
                result = int(decoder.decode_8bit_int())
            elif mb_type == 'uint16':
                result = int(decoder.decode_16bit_uint())
            elif mb_type == 'int16':
                result = int(decoder.decode_16bit_int())
            elif mb_type == 'uint32':
                result = int(decoder.decode_32bit_uint())
            elif mb_type == 'int32':
                result = int(decoder.decode_32bit_int())
            elif mb_type == 'uint64':
                result = int(decoder.decode_64bit_uint())
            elif mb_type == 'int64':
                result = int(decoder.decode_64bit_int())
            elif mb_type == 'float32' or mb_type == 'float':
                result = float(decoder.decode_32bit_float())
            elif mb_type == 'float64':
                result = float(decoder.decode_64bit_float())
            elif mb_type == 'bit':
                result = int(decoder.decode_bits())
            elif mb_type == 'bool':
                result = bool(raw[0])
            elif mb_type == 'raw':
                result = raw[0]
            else:
                result = raw
        except ValueError as e:
            #log.exception(e)
            result = raw
    return result


SERVER_HOST = "192.168.0.210"
SERVER_PORT = 502
SERVER_UNIT = 201

c = ModbusClient()



# uncomment this line to see debug message
c.debug(True)

# define modbus server host, port
c.host(SERVER_HOST)
c.port(SERVER_PORT)
c.unit_id(SERVER_UNIT)



if not c.is_open():
    if not c.open():
        print("unable to connect to "+SERVER_HOST+":"+str(SERVER_PORT))

# if open() is ok, read register (modbus function 0x03)
if c.is_open():
    # read 10 registers at address 0, store result in regs list
    regs = c.read_holding_registers(0, 10)
    # if success display registers
    if regs:
        print(encode_field(regs(0),'str'))
        print("reg ad #0 to 9: "+str(regs))

    # sleep 2s before next polling
