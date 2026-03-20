import socket
import time
from protocol import *

TIMEOUT = 0.5
CHUNK_SIZE = 1024
WINDOW_SIZE = 4  
MAX_SEQ = 256    

def send_file(filename, dest_ip, dest_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT)

    # Read all file chunks into a list
    packets = []
    seq = 0
    with open(filename, "rb") as f:
        while True:
            data = f.read(CHUNK_SIZE)
            if not data:
                break
            packets.append(make_packet(seq % MAX_SEQ, 0, FLAG_DATA, data))
            seq += 1

    total_packets = len(packets)
    base = 0  # seq of earliest unACKed packet
    next_seq = 0

    print(f"Total packets to send: {total_packets}")

    while base < total_packets:
        # send packets in window
        while next_seq < base + WINDOW_SIZE and next_seq < total_packets:
            sock.sendto(packets[next_seq], (dest_ip, dest_port))
            print(f"Sent packet {next_seq}")
            next_seq += 1

        try:
            ack_packet, _ = sock.recvfrom(2048)
            ack_seq, _, flags, _, _ = parse_packet(ack_packet)
            if flags & FLAG_ACK:
                print(f"Received ACK {ack_seq}")
                # Move base forward
                base = ack_seq + 1
        except socket.timeout:
            # Timeout: Go-Back-N retransmit from base
            print(f"Timeout, retransmitting from packet {base}")
            next_seq = base

    # Send FIN reliably
    fin_sent = False
    while not fin_sent:
        fin_packet = make_packet(seq % MAX_SEQ, 0, FLAG_FIN, b'')
        sock.sendto(fin_packet, (dest_ip, dest_port))
        print("Sent FIN")
        try:
            ack_packet, _ = sock.recvfrom(2048)
            ack_seq, _, flags, _, _ = parse_packet(ack_packet)
            if flags & FLAG_ACK:
                print("FIN acknowledged")
                fin_sent = True
        except socket.timeout:
            print("Timeout, retransmitting FIN")

    sock.close()


if __name__ == "__main__":
    send_file("input.txt", "127.0.0.1", 8000)