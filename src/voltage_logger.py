import pyvisa
import time
#import numpy as np
#import matplotlib.pyplot as plt
import datetime 
import csv
import json
import pathlib


class VoltageLogger:
    def __init__(self):
       config_path = pathlib.Path(__file__).parent / "config.json"
       with open(config_path, 'r') as f:
            config = json.load(f)
       self.HOST=config["host"]
       self.PORT=config["port"]
       self.TYPE=config["resource_type"]
       self.TIMESTEP=config["timestep"]  # in seconds
       self.FILENAME=f"voltage_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

       rm = pyvisa.ResourceManager()
       self.instrument = rm.open_resource(f"{self.TYPE}::{self.HOST}::{self.PORT}::SOCKET")
       print(f"Connected to instrument {self.HOST}:{self.PORT}")
       self.instrument.read_termination = '\n'
       self.instrument.write_termination = '\n'    
       self.instrument.timeout = config["timeout_ms"] # in milliseconds
       self.ID = self.instrument.query("*IDN?")
       print(f"Instrument ID: {self.ID}")

    def measure_voltage(self):
       return self.instrument.query("MEAS:VOLT?")

    def log_init(self):
        with open(self.FILENAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Voltage"])



            


if __name__ == "__main__":
    vl = VoltageLogger()
    vl.log_init() # Initialize log file with headers
    print(f"Logging voltage readings to {vl.FILENAME} every {vl.TIMESTEP} seconds.")
    with open(vl.FILENAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        while True: # Infinite loop to log voltage readings
            try:
                voltage = vl.measure_voltage() # Measure voltage
                timestamp = datetime.datetime.now().isoformat() # Current timestamp
                print(f"{timestamp}, {voltage}")
                writer.writerow([timestamp, voltage]) # Log the reading
                file.flush()  # Ensure data is written to file
                time.sleep(vl.TIMESTEP)  
            except KeyboardInterrupt:
                print("Logging stopped by user.")
                break
            except pyvisa.errors.VisaIOError as e:
                print(f"An error occurred: {e} Retrying...")
                time.sleep(vl.TIMESTEP)
                continue                   
            except Exception as e:
                print(f"An error occurred: {e}")
                print("Logging stopped.")
                break
            
    vl.instrument.close()
    print("Instrument connection closed.")
