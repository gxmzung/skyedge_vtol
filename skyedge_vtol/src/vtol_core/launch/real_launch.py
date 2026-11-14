"""Legacy physical-flight entry point intentionally disabled.

This repository currently contains a stub bridge, NOT a verified PX4 adapter.
Fail closed until independent hardware safety approval and implementation exist.
"""


def generate_launch_description():
    raise RuntimeError(
        "Real-aircraft launch is disabled: no verified PX4 vehicle adapter, "
        "operator safety path, or hardware-in-the-loop evidence. "
        "Use offline tests and a separately verified SITL environment only."
    )
