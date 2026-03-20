UDP Protocol:
Author: Elan A. Cote

This project implements a reliable file transfer protocol over UDP. Since UDP does not guarantee delivery, ordering, or integrity, this protocol adds reliability using:

Sliding window mechanism

Sequence numbers

Acknowledgments (ACKs)

Retransmissions on timeout

Checksum-based corruption detection

A network simulator is included to introduce packet loss, corruption, and reordering.

Project Structure
.
├── client.py        # Sends file (sender)
├── server.py        # Receives file (receiver)
├── simulator.py     # Simulates unreliable network
├── sender.py        # Core sending logic
├── receiver.py      # Core receiving logic
├── protocol.py      # Packet structure and helpers
├── input.txt        # Input file to send
├── output.txt       # Received output file
├── docs/            # Sphinx documentation
⚙️ Requirements

Python 3.x

Virtual environment (recommended)

📦 Installation
1. Create a virtual environment
python -m venv myenv
2. Activate it

Windows (PowerShell):

myenv\Scripts\activate

Mac/Linux:

source myenv/bin/activate
3. Install dependencies (if needed)
pip install -r requirements.txt

How to Run

You must run three components in separate terminals.

Terminal 1 — Start Server
python server.py

Expected output:

Server listening on port 9000...
Terminal 2 — Start Simulator
python simulator.py

Expected output:

Simulator listening on port 8000...

This simulates:

Packet loss

Packet corruption

Packet reordering

Terminal 3 — Run Client
python client.py

Expected output:

Sent packet 0
Received ACK 0
...
Input File

Edit input.txt to change what gets sent.

Example:

Hello World
This is a test of reliable UDP transfer.
Output File

After successful transfer, the received file will be saved as:

output.txt

How It Works
Sender

Splits file into chunks

Sends packets with sequence numbers

Waits for ACKs

Retransmits on timeout

Receiver

Receives packets

Checks for corruption

Writes in-order packets to file

Sends ACKs

Simulator

Randomly drops packets

Randomly corrupts packets

May reorder packets

Testing Reliability

To fully test the protocol:

Force multiple packets

Modify in sender.py:

CHUNK_SIZE = 50
Observe behavior:

"Packet dropped" → retransmission

"Packet corrupted" → detected and resent

Out-of-order packets handled correctly

