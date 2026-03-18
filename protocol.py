import struct
import hashlib

# Packet format:
# seq (I), ack (I), flags (B), checksum (32s), data (variable)
HEADER_FORMAT = "!IIB32s"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

FLAG_ACK = 1
FLAG_DATA = 2
FLAG_FIN = 4


def compute_checksum(data: bytes) -> bytes:
    return hashlib.md5(data).hexdigest().encode()


def make_packet(seq, ack, flags, data: bytes):
    checksum = compute_checksum(data)
    header = struct.pack(HEADER_FORMAT, seq, ack, flags, checksum)
    return header + data


def parse_packet(packet: bytes):
    header = packet[:HEADER_SIZE]
    data = packet[HEADER_SIZE:]

    seq, ack, flags, checksum = struct.unpack(HEADER_FORMAT, header)

    return seq, ack, flags, checksum, data


def is_corrupt(data, checksum):
    return compute_checksum(data) != checksum