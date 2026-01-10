# Voltage Logger (SCPI via PyVISA)

A Python-based utility for automated voltage data acquisition from instruments supporting SCPI (Standard Commands for Programmable Instruments) over a TCP/IP (Socket) connection.

## 🚀 Features

* **SCPI Communication:** Connects to instruments using PyVISA via TCPIP Socket.
* **Instrument Identification:** Automatically queries `*IDN?` upon connection to verify the device.
* **Real-time Logging:** Measures voltage using `MEAS:VOLT?` and logs data to a CSV file with high-precision ISO timestamps.
* **Graceful Shutdown:** Handles `KeyboardInterrupt` (Ctrl+C) to ensure the instrument connection is properly closed before the script exits.

## 📋 Prerequisites

Ensure you have the following installed:

1.  **Python 3.x**
2.  **Required Libraries:**
    ```bash
    pip install pyvisa pyvisa-py numpy matplotlib
    ```
3.  **VISA Backend:**
    * You can use [NI-VISA](https://www.ni.com/en-cz/support/downloads/drivers/download.ni-visa.html).
    * Alternatively, use the open-source **PyVISA-py** backend.

## ⚙️ Configuration

You can configure the connection and logging parameters directly within the `VoltageLogger` class in `voltage_logger.py`:

| Parameter | Default Value | Description |
| :--- | :--- | :--- |
| `HOST` | `127.0.0.1` | The IP address of your instrument. |
| `PORT` | `5025` | Communication port (standard SCPI port is usually 5025). |
| `TIMESTEP` | `0.5` | Delay between measurements (in seconds). |
| `FILENAME` | `voltage_log.csv` | The name of the output CSV file. |

## 🛠️ Usage

1.  **Connect your instrument** to the network and ensure you can ping its IP address.
2.  **Update the configuration** in the script (specifically the `self.HOST` variable).
3.  **Run the script:**
    ```bash
    python voltage_logger.py
    ```
4.  The script will display live readings in the console and append them to the CSV file simultaneously.
5.  **To stop logging**, press `Ctrl+C`. The script will catch the interrupt, close the instrument session safely, and exit.

## 📊 Data Output

Data is saved in a standard CSV format, compatible with Excel, MATLAB, or Python (Pandas/Matplotlib):

```csv
2026-01-10T14:30:05.123456, 1.2345
2026-01-10T14:30:05.623456, 1.2351
