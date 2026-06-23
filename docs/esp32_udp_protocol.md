# ESP32 UDP Vision Protocol

## Message Format

```text
TARGET=1,OX=0.12,OY=-0.04,CONF=0.91

Fields
Field	Meaning
TARGET	1 if target detected, 0 otherwise
OX	horizontal target offset from image center
OY	vertical target offset from image center
CONF	detection confidence
Example
TARGET=1,OX=-0.15,OY=0.07,CONF=0.87
Integration Idea

The mission stack can use this message to decide whether to assist:

target approach
precision landing
search zone confirmation
visual guidance alignment
Safety Boundary

Vision packets must not directly override PX4 control.

They should be treated as advisory input for the mission layer.

```
