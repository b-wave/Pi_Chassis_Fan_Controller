# Example Scripts
These were generated scripts and some are not really tested. But you should be able to modify for your own use. 
--

## The Hardware Test Python Script 

**[fan_thermal_test.py]**

This Python script uses the **gpiozero** library to test the fan and the PCB. It reads the Pi SoC and the ambient temperature (via the RTC module). This script does work on my hardware but you may need to modify it to run. You should see a smooth linear climb for example: 
  
*Start at 0% duty cycle climbing to 750 RPM at 25% duty cycle up to a whopping 3,900 RPM at 100% means your PCB's hardware pull-up circuit and the software interrupt logic are working flawlessly.*


NOTE: 

- Some settings I used on my Raspberry Pi 3 system is running a development branch of Debian Trixie (Debian 13) with Linux kernel 6.18.34+rpt-rpi-v8
-   While 25,000 Hz (25kHz) is the ideal hardware standard for computer fans to prevent a high-pitched whining noise, a software-driven GPIO pin using lgpio cannot handle a frequency that high and throws a 'bad PWM frequency' error. So to bypass this error and see the fan spin, we can change the frequency down to a standard value that lgpio accepts, like 100 Hz. Because 100 Hz is in the human audible spectrum, the fan motor might make a faint humming sound during the test—this is completely normal for software PWM!
-   Also, the interface board has its own pull up resistor on the TACH line, so I turned off the pull up on the GPIO as well. 
   
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
--
