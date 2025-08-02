# Simple logic: if a MAC address appears too frequently → suspicious

from collections import defaultdict
from datetime import datetime, timedelta

mac_activity = defaultdict(list)
THRESHOLD = 10  # max 10 deauth per minute

def is_suspicious(mac):
    now = datetime.now()
    mac_activity[mac] = [ts for ts in mac_activity[mac] if now - ts < timedelta(minutes=1)]
    mac_activity[mac].append(now)
    return len(mac_activity[mac]) > THRESHOLD
