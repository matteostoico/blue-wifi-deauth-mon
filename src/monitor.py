from scapy.all import sniff, Dot11, RadioTap
from utils.detection import is_suspicious
from datetime import datetime
import os
import csv

LOG_FILE = "logs/deauth_log.csv"
IFACE = "wlan0mon"  # network to sniff

def ensure_log_dir():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    if not os.path.isfile(LOG_FILE):
        with open(LOG_FILE, mode='w') as f:
            writer = csv.writer(f)
            writer.writerow(['Timestamp', 'Source MAC', 'Destination MAC', 'RSSI', 'Channel', 'Suspicious'])

def log_packet(src, dst, rssi, channel, suspicious):
    timestamp = datetime.now().isoformat()
    with open(LOG_FILE, mode='a') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, src, dst, rssi, channel, suspicious])
    flag = "⚠️ Suspicious" if suspicious else "OK"
    print(f"[{timestamp}] Deauth -> From: {src} To: {dst} | RSSI: {rssi} | Ch: {channel} | {flag}")

def parse_packet(packet):
    if packet.haslayer(Dot11):
        dot11 = packet.getlayer(Dot11)
        if dot11.type == 0 and dot11.subtype == 12: # type 0 (management), subtype 12 (deauth)
            src = dot11.addr2
            dst = dot11.addr1
            try:
                rssi = packet.dBm_AntSignal # try to detect the signal power, otherwise N/A
            except:
                rssi = "N/A"
            try:
                channel = int(ord(packet[RadioTap].notdecoded[14:15])) # try to detect the channel, otherwise ? - can change depending on hardware
            except:
                channel = "?"
            suspicious = is_suspicious(src) # function from detection.py
            log_packet(src, dst, rssi, channel, suspicious)

if __name__ == "__main__":
    print("[*] Starting Wi-Fi Spectrum Surveillance (Deauth Monitor)")
    print("[*] Press CTRL+C to stop.\n")
    ensure_log_dir()
    sniff(iface=IFACE, prn=parse_packet, store=0)
