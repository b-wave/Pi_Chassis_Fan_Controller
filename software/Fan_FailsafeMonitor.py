import time
from gpiozero import Button
import subprocess

# --- CONFIGURATION ---
TACH_PIN = 23          # Change to whichever GPIO pin you used
PULSES_PER_REV = 2     # Standard PC/chassis fans output 2 pulses per revolution
CHECK_INTERVAL = 3.0   # How often to check the fan status (seconds)

# Keep track of pulses detected by the pin
pulse_count = 0

def count_pulse():
    global pulse_count
    pulse_count += 1

# Initialize the pin using gpiozero's Button class
# This automatically enables the safe internal 3.3V pull-up resistor
tach_wire = Button(TACH_PIN, pull_up=True)
tach_wire.when_pressed = count_pulse

print("Failsafe monitoring started. Watching for fan stalls...")

try:
    while True:
        # Reset pulse counter and wait for the tracking interval
        pulse_count = 0
        time.sleep(CHECK_INTERVAL)
        
        # Calculate RPM
        # Formula: (Pulses / Seconds) * 60 seconds / Pulses Per Revolution
        frequency = pulse_count / CHECK_INTERVAL
        rpm = (frequency * 60) / PULSES_PER_REV
        
        print(f"Current Fan Speed: {int(rpm)} RPM")
        
        # --- STALL DETECTION LOGIC ---
        # If the fan reads 0 RPM, execute safety fallback commands
        if rpm == 0:
            print("WARNING: Fan stall detected! Engaging power-saving mode.")
            
            # Example: Force Raspberry Pi CPU into low-power 'powersave' governor
            # (Requires running script with sudo)
            subprocess.run([
                "sudo", "cpufreq-set", "-g", "powersave"
            ], capture_output=True)
            
            # Alternate option: You could trigger a safe shutdown instead
            # subprocess.run(["sudo", "shutdown", "-h", "now"])
            
            break # Exit script after triggering failsafe

except KeyboardInterrupt:
    print("\nMonitoring stopped by user.")
