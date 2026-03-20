import socket
import random

LOSS_RATE = 0.2
CORRUPT_RATE = 0.2

CLIENT_ADDR = None
SERVER_ADDR = ("127.0.0.1", 9000)


def corrupt_packet(packet):
    packet = bytearray(packet)
    if len(packet) > 0:
        packet[0] ^= 0xFF
    return bytes(packet)


def run_simulator(listen_port):
    global CLIENT_ADDR

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", listen_port))

    print(f"Simulator listening on port {listen_port}...")

    while True:
        try:
            packet, addr = sock.recvfrom(2048)
        except ConnectionResetError:
            print("Connection reset (client/server closed)")
            continue

        # Identify sender
        if addr != SERVER_ADDR:
            CLIENT_ADDR = addr
            destination = SERVER_ADDR
            direction = "Client → Server"
        else:
            destination = CLIENT_ADDR
            direction = "Server → Client"

        print(f"{direction}")

        # Simulate loss
        if random.random() < LOSS_RATE:
            print("Packet dropped")
            continue

        # Simulate corruption
        if random.random() < CORRUPT_RATE:
            print("Packet corrupted")
            packet = corrupt_packet(packet)

        sock.sendto(packet, destination)


if __name__ == "__main__":
    run_simulator(8000)