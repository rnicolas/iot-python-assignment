#!/usr/bin/env python3

import struct
import logging
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.exceptions import ConnectionException, ModbusIOException

UNIT = 0x1
ADDRESS = "192.168.0.102"

def uint16_to_float(uint1, uint2):
    # Pack the two uint16 values into a binary string
    packed_data = struct.pack('HH', uint1, uint2)
    
    # Unpack the binary string as a single float
    float_number = struct.unpack('f', packed_data)[0]
    
    return float_number

def read_data(start_register, connector, channel):
    register_to_be_read = start_register + ((connector - 1) * 3 + channel - 1) * 2
    registers = read_registers(register_to_be_read, 2)
    if registers:
        uint1, uint2 = registers
        return uint16_to_float(uint1, uint2)
    else:
        return None

def read_registers(register, number):
    MAX_RETRIES = 3
    for retry in range(MAX_RETRIES):
        try:
            client = ModbusClient('192.168.0.102')
            client.connect()

            # Read the registers
            resp = client.read_input_registers(register, number, unit=UNIT)

            # Close the connection
            client.close()

            # Return the response
            return resp.registers

        except ConnectionException as e:
            print("Modbus connection error:", e)
        
        except ModbusIOException as e:
            print("Modbus I/O error:", e)
    return None

def read_rms_voltage(connector, channel):
    start_register = 352
    return read_data(start_register, connector, channel)

def read_frequency(connector, channel):
    start_register = 424
    return read_data(start_register, connector, channel)

def read_active_energy_import_index(connector, channel):
    start_register = 28
    return read_data(start_register, connector, channel)

def read_reactive_energy_import_index(connector, channel):
    start_register = 64
    return read_data(start_register, connector, channel)

def read_active_energy_export_index(connector, channel):
    start_register = 100
    return read_data(start_register, connector, channel)

def read_reactive_energy_export_index(connector, channel):
    start_register = 136
    return read_data(start_register, connector, channel)

def read_active_power(connector, channel):
    start_register = 172
    return read_data(start_register, connector, channel)

def read_reactive_power(connector, channel):
    start_register = 208
    return read_data(start_register, connector, channel)

def read_power_factor(connector, channel):
    start_register = 244
    return read_data(start_register, connector, channel)

def read_rms_current(connector, channel):
    start_register = 280
    return read_data(start_register, connector, channel)

def read_rms_current_1_min_average(connector, channel):
    start_register = 316
    return read_data(start_register, connector, channel)

def read_rms_voltage_1_min_average(connector, channel):
    start_register = 388
    return read_data(start_register, connector, channel)
