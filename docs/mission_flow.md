# Mission Flow

## Normal Mission

```text
IDLE -> ARMING -> TAKEOFF -> MISSION -> RETURN_HOME -> LANDING -> COMPLETE

Failsafe Mission

Any unsafe telemetry condition can interrupt the mission:

ANY_STATE -> FAILSAFE
Failsafe Conditions
Condition	Rule
Low battery	battery < 25%
Low signal	signal < 40
GPS unsafe	satellites < 8
High temperature	temperature > 75
Altitude unsafe	altitude < 0 or altitude > 120