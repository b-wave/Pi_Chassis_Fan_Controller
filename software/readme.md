
# The Failsafe Monitoring Script

This Python script uses the gpiozero library to watch for pulses on the FG pin. It calculates the RPM, and if the fan is supposed to be running but stalls out (RPM drops to 0), it triggers your power-saving protective mode