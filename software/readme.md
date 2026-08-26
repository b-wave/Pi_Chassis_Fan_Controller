# Example Scripts
These were generated scripts and not tested. But you shoud be able to modify for your own use. 
--

**[fan_thermal_test.py]**

This Python script uses the gpiozero library to test the fan and the PCB. It reads ther SoC and the ambient temperature (via the RTC module)  I was seeing a smooth linear climb from 750 RPM at 25% duty cycle up to a whopping 3,900 RPM at 100% means your PCB's hardware pull-up circuit and the software interrupt logic are working flawlessly. 

NOTE: 

```
# 25kHz is the industrial standard target frequency for 4-wire fans
fan_pwm = PWMOutputDevice(PWM_PIN, frequency=100, initial_value=0.0)
fan_tach = DigitalInputDevice(TACH_PIN, pull_up=None, active_state=False) # Using the PCB's 3V3 hardware pull-up
```

## The Failsafe Monitoring Python Script

**[Fan_Failsafe_Monitor.py]**

This Python script uses the gpiozero library to watch for pulses on the FG pin. It calculates the RPM, and if the fan is supposed to be running but stalls out (RPM drops to 0), it triggers your power-saving protective mode

--
## System Test with Logging and Alerts Python Script

**[Fan_System_Test_Example.py]**
This is an example operational/test script hat reads temperatures from two points in the chassis, the SoC and the ambient temperature (the termal sensor in the RTC chip) to help define and set the setpoints.  The test's alerts are shown with ntfy.com  

--
##  Complete Automated Python Script

**[Fan_Control.py]**
This script uses the gpiozero library to handle both pins. It samples the Raspberry Pi's internal CPU temperature every few seconds. If the Pi gets warm, it turns on the fan and scales the fan's speed using PWM. If the Pi cools down, it shuts off the fan completely  (PWM = 0%) to save power.