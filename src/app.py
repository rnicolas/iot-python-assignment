#!/usr/bin/env python3
"""
A simple ModbusTCP - HTTP app
"""

import exporter_ecoadapt as ecoadapt
import sender
import argparse
import time

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="EcoAdapter Modbus <-> Websocket",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument("-t", "--time", type=float, default=1.5, help="Time in ms between readouts")

        args = vars(parser.parse_args())
        t = args['time']

        while True:

            # Read from Modbus
            try:
                rms_voltage = ecoadapt.read_rms_voltage(1, 1)
                if rms_voltage is not None:
                    print("RMS Voltage: ", rms_voltage)
                else:
                    print("Failed to read RMS Voltage.")
            except Exception as e:
                print("An error occurred:", e)

            try:
                frequency = ecoadapt.read_frequency(1, 1)
                if frequency is not None:
                    print("Frequency: ", frequency)
                else:
                    print("Failed to read Frequency.")
            except Exception as e:
                print("An error occurred:", e)

            # Send the information received to server
            if rms_voltage is not None and frequency is not None:
                msg = "{\"rms_voltage\": "+ str(rms_voltage) +", \"frequency\":"+ str(frequency) +"}"
                sender.send_message(msg)
            
            time.sleep(t)

    except KeyboardInterrupt:
        print( "\rExit." )
