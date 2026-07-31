# Example Scripts
These were generatedscripts and not tested. But you shoudbe abel to modify for your own use. 
--

## The Failsafe Monitoring Python Script

This Python script uses the gpiozero library to watch for pulses on the FG pin. It calculates the RPM, and if the fan is supposed to be running but stalls out (RPM drops to 0), it triggers your power-saving protective mode

--
## The Complete Automated Python Script

This script uses the gpiozero library to handle both pins. It samples the Raspberry Pi's internal CPU temperature every few seconds. If the Pi gets warm, it turns on the transistor and scales the fan speed using PWM. If the Pi cools down, it shuts off the transistor completely to save power.