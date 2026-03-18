import socket
import time
from protocol import *

TIMEOUT = 0.5
CHUNK_SIZE = 1024


def send_file(filename, dest_ip, dest_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT)

    with open(filename, "rb") as f:
        seq = 0

        while True:
            data = f.read(CHUNK_SIZE)
            if not data:
                break

            packet = make_packet(seq, 0, FLAG_DATA, data)

            while True:
                sock.sendto(packet, (dest_ip, dest_port))
                print(f"Sent packet {seq}")

                try:
                    ack_packet, _ = sock.recvfrom(2048)
                    ack_seq, _, flags, _, _ = parse_packet(ack_packet)

                    if flags & FLAG_ACK and ack_seq == seq:
                        print(f"Received ACK {ack_seq}")
                        break

                except socket.timeout:
                    print(f"Timeout, retransmitting {seq}")

            seq += 1

        # Send FIN
        while True:
            fin_packet = make_packet(seq, 0, FLAG_FIN, b'')
            sock.sendto(fin_packet, (dest_ip, dest_port))
            print("Sent FIN")

            try:
                ack_packet, _ = sock.recvfrom(2048)
                ack_seq, _, flags, _, _ = parse_packet(ack_packet)

                if flags & FLAG_ACK:
                    print("FIN acknowledged")
                    break

            except socket.timeout:
                print("Timeout, retransmitting FIN")

    sock.close()


if __name__ == "__main__":
    send_file("input.txt", "127.0.0.1", 9000)

from sender import send_file

from receiver import receive_file

