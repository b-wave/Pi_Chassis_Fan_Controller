# Example Scripts
These were generatedscripts and not tested. But you shoud be abel to modify for your own use. 
--

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
