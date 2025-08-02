# Wi-Fi Deauthentication Packet Monitor

A Python-based network surveillance tool that monitors the wireless spectrum for deauthentication (Deauth) packets, logs them, and flags potentially suspicious activity. This tool is designed for Blue Team use cases such as intrusion detection, Evil Twin attack monitoring, and DoS defense.

## Features

- Real-time monitoring of 802.11 Deauth packets
- CSV logging with timestamp, MAC addresses, RSSI, and channel
- Suspicious activity detection using basic heuristics
- Console alerts for high-volume deauthentication attempts
- Modular structure for easy extensibility

## Requirements

- Linux system with a wireless interface capable of monitor mode
- Python 3.6 or higher
- aircrack-ng (to enable monitor mode on your wireless interface)
- Scapy (https://scapy.net/)
- Root privileges

## Setup

### 1. Enable monitor mode using airmon-ng:

Make sure `aircrack-ng` is installed:

```bash
sudo apt install aircrack-ng
```

Enable monitor mode: 

```bash
sudo airmon-ng start wlan0
```

Check that a new monitor interface (e.g., wlan0mon) has been created:

```bash
iwconfig
```

Replace `wlan0` with the name of your wireless interface.

### 2. Clone the repository

```bash
git clone https://github.com/matteostoico/wifi-deauth-mon.git
cd wifi-deauth-monitor
```

### 3. Install dependencies


```bash
sudo apt update
sudo apt install python3-pip
sudo pip3 install -r requirements.txt --break-system-packages
```

## Usage

Important: Set the Correct Wi-Fi Channel

To properly capture management packets such as deauthentication, your Wi-Fi interface in monitor mode must be tuned to the same channel used by the target network.

Find the Wi-Fi channel used by your network interface

```bash
sudo iw dev wlan0 info
```
If your monitor interface is wlan0mon, set its channel with:

```bash
sudo iw dev wlan0mon set channel <channel_number>
```
Then run the monitor script (as a module, from the project rood folder): 

```bash
sudo python3 -m src.monitor
```
Note: Before running the script, open src/monitor.py and replace all occurrences of wlan0 with the name of your wireless interface in monitor mode (e.g., wlan0mon), which you can find by running iwconfig.

Example output:

```
[*] Starting Wi-Fi Spectrum Surveillance (Deauth Monitor)
[*] Press CTRL+C to stop.

[2025-08-02T09:15:42.011Z] Deauth -> From: AA:BB:CC:DD:EE:FF To: FF:EE:DD:CC:BB:AA | RSSI: -52 | Ch: 6 | Suspicious
```

All events are saved in `logs/deauth_log.csv`, including:

|           Timestamp       | Source MAC | Destination MAC | RSSI | Channel | Suspicious |
|---------------------------|------------|-----------------|------|---------|------------|
| 2025-08-02T09:15:42.011Z  |  AA:BB:... | FF:EE:...       | -52  |    6    |    True    |

## Detection Logic

Deauthentication attacks are characterized by a high number of deauth packets in a short period. The tool tracks the number of deauth packets per source MAC address over a rolling 60-second window. If a device exceeds a configurable threshold (default: 10 deauths per minute), it is flagged as suspicious.

Heuristics are implemented in `utils/detection.py`.

## Project Structure

```
blue-wifi-deauth-mon/
├── src/                # Main script
│   └── monitor.py
├── utils/              # Detection logic
│   └── detection.py
├── logs/               # CSV logs
│   └── deauth_log.csv
├── requirements.txt    # Python dependencies
├── .gitignore
└── README.md
```

## Possible Improvements

- Real-time alerts via email, Telegram, or webhook
- Integration with Splunk or ELK stack for centralized logging
- Dashboard with Streamlit, Dash, or Grafana
- MAC spoofing detection
- Beacon and probe request analysis

## Author

**Matteo Stoico**
IT Project Manager | Blue Team Cybersecurity Enthusiast
Based in Spain

[LinkedIn](https://linkedin.com/in/matteostoico)
Email: matteo.stoico@live.it

## License

This project is licensed under the MIT License. See the LICENSE file for details.
