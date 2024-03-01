"""
A minimal EcoAdapt modbus reader
"""

import struct
import logging
from .exporter_ecoadapt import *
from pymodbus.exceptions import ConnectionException, ModbusIOException

# Configure the client logging
FORMAT = (
    "%(asctime)-15s %(threadName)-15s "
    "%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s"
)
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.INFO)

__all__ = [
    'read_rms_voltage', 'read_frequency', 'read_active_energy_import_index',
    'read_reactive_energy_import_index', 'read_active_energy_export_index',
    'read_reactive_energy_export_index', 'read_active_power', 'read_reactive_power',
    'read_power_factor', 'read_rms_current', 'read_rms_current_1_min_average',
    'read_rms_voltage_1_min_average'
]