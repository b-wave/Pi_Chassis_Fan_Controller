import time
from gpiozero import PWMOutputDevice, OutputDevice, CPUTemperature

# --- CONFIGURATION ---
PWM_PIN = 12       # GPIO Pin connected directly to the fan's 3rd wire
ENABLE_PIN = 13    # GPIO Pin connected to the 1kΩ resistor -> NPN Transistor Base

TEMP_MIN = 50.0    # Temperature (°C) where the fan turns on at lowest speed
TEMP_MAX = 70.0    # Temperature (°C) where the fan hits 100% maximum speed

# --- INITIALIZATION ---
# Active_high=True means setting the pin to True turns the transistor ON
fan_power = OutputDevice(ENABLE_PIN, active_high=True, initial_value=False)

# Initialize PWM with a standard 25kHz frequency suitable for fan controllers
fan_speed = PWMOutputDevice(PWM_PIN, frequency=25000, initial_value=0.0)

cpu = CPUTemperature()

print("Automated thermal chassis management started...")

try:
    while True:
        current_temp = cpu.temperature
        print(f"Current CPU Temp: {current_temp:.1f}°C")

        if current_temp < TEMP_MIN:
            # Pi is cool: Shut off PWM and cut the transistor ground completely
            fan_speed.value = 0.0
            fan_power.off()
            print("Chassis Cool: Fan completely powered down.")
            
        else:
            # Pi is warm: Ensure the transistor is active and grounding the fan
            if not fan_power.value:
                fan_power.on()
                time.sleep(0.1) # Brief pause to let power stabilize
            
            # Linear scaling formula to map temperature to a 0.0 - 1.0 PWM range
            scaled_speed = (current_temp - TEMP_MIN) / (TEMP_MAX - TEMP_MIN)
            
            # Constrain the speed between 20% minimum (to keep it spinning) and 100% max
            target_pwm = max(0.2, min(1.0, scaled_speed))
            
            fan_speed.value = target_pwm
            print(f"Chassis Warm: Fan power active. Speed set to {int(target_pwm * 100)}%")

        # Wait 5 seconds before sampling the temperature again
        time.sleep(5.0)

except KeyboardInterrupt:
    print("\nStopping script. Resetting fan pins...")
    fan_speed.close()
    fan_power.close()
