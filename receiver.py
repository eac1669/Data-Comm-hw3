import socket
import time
from protocol import *

OUTPUT_FILE = "output.txt"


def receive_file(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", port))

    print(f"Server listening on port {port}...")

    expected_seq = 0

    with open(OUTPUT_FILE, "wb") as f:
        while True:
            packet, addr = sock.recvfrom(2048)

            seq, _, flags, checksum, data = parse_packet(packet)

            if is_corrupt(data, checksum):
                print("Corrupt packet dropped")
                continue

            if flags & FLAG_FIN:
                print("File transfer complete")

                # Send ACK for FIN
                ack_packet = make_packet(seq, 0, FLAG_ACK, b'')
                sock.sendto(ack_packet, addr)

                # Stay alive briefly to handle retransmissions
                for _ in range(3):
                    try:
                        sock.settimeout(0.5)
                        packet, addr = sock.recvfrom(2048)
                        seq2, _, flags2, _, _ = parse_packet(packet)

                        if flags2 & FLAG_FIN:
                            sock.sendto(ack_packet, addr)

                    except socket.timeout:
                        break

                break

            if seq == expected_seq:
                f.write(data)
                print(f"Received packet {seq}")
                expected_seq += 1

            # Send ACK
            ack_packet = make_packet(seq, 0, FLAG_ACK, b'')
            sock.sendto(ack_packet, addr)

    sock.close()


if __name__ == "__main__":
    receive_file(9000)