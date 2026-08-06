import os
import time
import subprocess
import requests
from datetime import datetime

# CONFIGURATION PARAMETERS
NTFY_TOPIC = "[your_ntfy_topic]"  # <-- Replace with your exact topic string
LOG_DIR = "/var/log/telemetry"
SOC_THRESHOLD = 140.0   # SoC Alert Limit (°F)
RTC_THRESHOLD = 115.0   # Ambient Box Alert Limit (°F)

os.makedirs(LOG_DIR, exist_ok=True)

def read_soc_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            celsius = float(f.read().strip()) / 1000.0
            return (celsius * 9.0 / 5.0) + 32.0
    except: return 0.0

def read_rtc_temp():
    try:
        # Pulls from native hardware monitor node matched to your DS3231 crystal
        with open("/sys/class/hwmon/hwmon1/temp1_input", "r") as f:
            celsius = float(f.read().strip()) / 1000.0
            return (celsius * 9.0 / 5.0) + 32.0
    except:
        return 0.0

def dispatch_alert(message):
    try:
        requests.post(f"https://ntfy.sh{NTFY_TOPIC}", 
                      data=message.encode('utf-8'),
                      headers={"Title": "⚠️ Gateway Thermal Alert", "Priority": "high"})
    except:
        pass

# Initialize tracking baseline
alert_sent = False

while True:
    soc_f = read_soc_temp()
    rtc_f = read_rtc_temp()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = os.path.join(LOG_DIR, f"telemetry_{datetime.now().strftime('%Y-%m-%d')}.csv")
    
    # Write header if file is fresh
    if not os.path.exists(log_file):
        with open(log_file, "w") as f:
            f.write("Timestamp,SoC_Temp_F,RTC_Temp_F,Fan_RPM\n")
            
    # Dummy placeholder for Fan RPM until your interface board mounts
    current_rpm = 0 
    
    # Append current telemetry line
    with open(log_file, "a") as f:
        f.write(f"{timestamp},{soc_f:.2f},{rtc_f:.2f},{current_rpm}\n")
        
    # Evaluate safety parameters
    if (soc_f > SOC_THRESHOLD or rtc_f > rtc_threshold) and not alert_sent:
        msg = f"Critical Heat Detected!\nSoC: {soc_f:.1f}°F\nBox Ambient: {rtc_f:.1f}°F\nExecuting active thermal safety flush."
        dispatch_alert(msg)
        alert_sent = True
    elif (soc_f < (SOC_THRESHOLD - 5)) and (rtc_f < (RTC_THRESHOLD - 5)):
        alert_sent = False # Reset flag when temps drop safely
        
    time.sleep(10) # Log sweep every 10 seconds
