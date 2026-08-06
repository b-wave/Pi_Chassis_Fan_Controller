# A Pi Chassis Fan Controller - Interface Board 
This describes a small board to interface a 5V, 4-wire fan in a controller cabinet with a Raspberry Pi controller.  The fan I am using is a **GeekPi** 40x40x10mm 4-wire Fan, **Model F-0028**.  

The JST SH connector on the board should be compatible with the rPi's Fan Connector. You do not need this to control the processor fan, it is intended to actively ventilate an enclosed, wall mounted cabinet. 

Although I provide a separate 2-pin input voltage connector terminal block (J3) it is intended for 5-Volts only. Its purpose is to not stress the **Raspberry Pi4's** Power supply.  Although it should be perfectly fine to run the recommended fan directly off of the Pi +5V, since it was designed to run off of the fan connector on the newer Pi boards. 

By the way, that connector is reverse voltage protected in case you get the power leads reversed - you *should not* damage the Pi.

### ⚡ CAUTION ⚡
Be careful if using a 12V fan! *Damage may occur to 3v3 inputs and you may fry your Pi.* 

It may need  a **level shifter** if it does not provide 5V or pin compatible signals (TACH and maybe the PWM) - verify pin voltages before connecting to PI.  If they are open collector the 3v3 reference on the 10k pullup should take care of that. 

<p align="center">
  <img src="resources/fan_controller_revc.png" width="350" alt="3D View Generated">
</p>

## Overview
I am working on a Raspberry Pi 4 controlled LTE gateway using a small DIN rail enclosure.  The planned locations are at fairly remote and the equipment will be enclosed in a small cabinet so active ventilation is required.  This board was needed to simplify installation and to provide some visual and remote feedback.  This is a fairly simple board that is tailored to my specific installations but I may expand it to be more general purpose.  In any case it provides a neat interface to control a cabinet fan



<p align="center">
  <img src="resources/fan_controller_revc.svg" width="600" alt="Schematic">
</p>

The schematic is pretty straightforward.  It uses a hybrid SMT + Through-hole technologies. 

---

## Hardware Description
The hardware combines familiar building blocks with a some added protection from the warm and dry environment.  Extras such as a static ring ground and ESD diodes are probably overkill but it is cheap insurance.  

  *I am not 100% sure if the "Ring Ground" is implemented correctly.  ...But it looks cool?*

<p align="center">
  <img src="resources/f2cf50859baaec17621ed978b20d583c.png" width="250" alt="CO400 PCB">
</p>

It is a approximately one inch square and is designed to fit on a small DIN rail carrier. The board is available on OSHPARK Shared and I will leave a link. [ www.oshpark](https://oshpark.com)

            Hole Spacing: 0.75" x 0.80" (19.0mm x 20.3mm)
            Board Outline: 1.10" x 1.20" (27.6mm x 30.2 mm)
The LEDs give a visual indication of the fan's operation, since in many cases the fan cannot be heard. 

### Wiring: 
The fan controller interface board has screw blocks, simply strip your wire tips back 1/8", slide them into the screw terminals, and screw to clamp them down tightly:

 - Fan 5V Power (J3) Pin (1) (Red) ──► Screw into terminal 5V (Pin 2 or 4)
 - Fan 5V Ground (J3) Pin (2) (Black) ──► Screw into terminal GND (Pin 6, 9, or 14)
   - ***NOTE:**  J3 pins may be to a second 5V supply as well*

 - Fan 3 Volt Reference (RED) ──► Screw into terminal (3V3)
 - Fan PWM Control Signal (Blue) ──► Screw into terminal GPIO 12 (Pin 32)
 - Fan System Ground (Black) ──► Screw into terminal GND (Pin 6, 9, or 14)
 - Fan TACH (or FG) Speed Feedback (Yellow) ──► Screw into terminal GPIO 13 (Pin 33)
   - ***NOTE:**  The colors are failrly standard - but they should match the Pi-Fan connectors*

### The "ON" LED: 
      
The "Fan On" or "Drive" Indicator (Green)

This LED is wired to the PWM lines powering the fan. When the fan is running at full speed (100% PWM) it is ON full, when it is OFF ( 0% PWM) the fan is OFF. There is a slight dim glow green whenever the fan has power and is being driven by the PWM signal in different speeds it also changes brightness. This LED can also be used to FLASH a code if the fan stalls to aid in servicing since it is strictly an output. 
  
### The "RUN" LED: 
The "Fan Spinning" Indicator (Yellow or Blue). 

This LED is wired to the TACH  line to monitor it visually. Sometimes this signal is labeled Frequency Generator (FG). 

When the fan is stalled or off, the LED either stays solid or completely dark. When the fan spins at high speed (e.g., 3000 RPM), the TACH pulses occur so quickly (100 times per second) that human eyes perceive the flashing as a continuous, soft glow. If the fan slows down or begins to struggle, you will visually notice the light dimming or starting to flicker.

---

## Example Software

*Coming Soon! - no, really.  Check back*
