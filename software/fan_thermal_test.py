#!/usr/bin/env python3
import time
import os
import sys
from gpiozero import PWMOutputDevice, DigitalInputDevice

# --- CONFIGURATION ---
PWM_PIN = 5   # Fan PWM Speed line
TACH_PIN = 6  # Fan Tachometer pulse line
PULSES_PER_REV = 2

# --- HW MON FILE MAPPINGS ---
# From your system logs: hwmon0 = cpu_thermal, hwmon1 = ds3231
CPU_TEMP_PATH = "/sys/class/hwmon/hwmon0/temp1_input"
RTC_TEMP_PATH = "/sys/class/hwmon/hwmon1/temp1_input"

# --- INITIALIZATION ---
# 25kHz is the industrial standard target frequency for 4-wire fans
fan_pwm = PWMOutputDevice(PWM_PIN, frequency=100, initial_value=0.0)
fan_tach = DigitalInputDevice(TACH_PIN, pull_up=None, active_state=False) # Using your PCB's 3V3 hardware pull-up

pulse_count = 0

def count_pulse():
    global pulse_count
    pulse_count += 1

fan_tach.when_activated = count_pulse

def read_thermal_sensors():
    """Reads system thermal data directly from kernel hwmon interfaces."""
    try:
        with open(CPU_TEMP_PATH, "r") as f:
            cpu_raw = int(f.read().strip())
    except Exception:
        cpu_raw = 0

    try:
        with open(RTC_TEMP_PATH, "r") as f:
            rtc_raw = int(f.read().strip())
    except Exception:
        rtc_raw = 0

    # Convert milli-Celsius strings (e.g., 28000) to standard Celsius float
    return cpu_raw / 1000.0, rtc_raw / 1000.0

def read_rpm(duration=2.0):
    """Calculates active fan RPM over an interrupt timing window."""
    global pulse_count
    pulse_count = 0
    time.sleep(duration)
    current_pulses = pulse_count
    rpm = (current_pulses / duration) * 60 / PULSES_PER_REV
    return int(rpm)

# --- EXECUTION LOOP ---
try:
    print("====================================================")
    print("      COMBINED THERMAL & FAN TEST RUN")
    print("====================================================")

    # 1. Read baseline ambient temperatures before starting fan
    cpu_t, rtc_t = read_thermal_sensors()
    print(f"[+] Initial Enclosure Core Temp: {cpu_t}°C")
    print(f"[+] Initial Enclosure Ambient (RTC): {rtc_t}°C\n")

    # 2. Cycle fan through discrete speeds to verify hardware tracking
    test_speeds = [0.0, 0.25, 0.50, 0.75, 1.0]
    for speed in test_speeds:
        print(f"Setting Fan PWM Duty Cycle: {int(speed * 100)}%")
        fan_pwm.value = speed

        print(" -> Stabilizing fan dynamics (5s)...")
        time.sleep(5)

        rpm = read_rpm(duration=2.0)
        cpu_t, rtc_t = read_thermal_sensors()
        print(f" -> [TACH]: {rpm} RPM | [SoC]: {cpu_t}°C | [RTC]: {rtc_t}°C\n")

    print("====================================================")
    print("Test complete. Returning fan control to default state.")

finally:
    fan_pwm.close()
    fan_tach.close()
    