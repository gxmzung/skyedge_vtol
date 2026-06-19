import socket
import time


TARGET_IP = "127.0.0.1"
TARGET_PORT = 4210


def build_vision_packet(target: int, offset_x: float, offset_y: float, confidence: float) -> str:
    return f"TARGET={target},OX={offset_x:.2f},OY={offset_y:.2f},CONF={confidence:.2f}"


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    samples = [
        (1, 0.12, -0.04, 0.91),
        (1, 0.08, -0.02, 0.94),
        (0, 0.00, 0.00, 0.12),
        (1, -0.15, 0.07, 0.87),
    ]

    for sample in samples:
        message = build_vision_packet(*sample)
        sock.sendto(message.encode("utf-8"), (TARGET_IP, TARGET_PORT))
        print(f"sent: {message}")
        time.sleep(1.0)

    sock.close()


if __name__ == "__main__":
    main()