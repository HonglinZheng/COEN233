import socket
from datetime import datetime
# connect with client
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.sendto("hello client".encode("utf-8"), ('127.0.0.1', 12345))

# global variable for the segment_no of successfully received message
# initialized as -1, means haven't received any message
seq_num = -1

# global variables: the essential elements of ack/reject packet
ACK = int("0xfff2", 16)
REJECT = int("0xfff3", 16)
REJECT_out_of_sequence = int("0xfff4", 16)
REJECT_length_mismatch = int("0xfff5", 16)
REJECT_End_of_packet_missing = int("0xfff6", 16)
REJECT_Duplicate_packet = int("0xfff7", 16)
Start_of_Packet_id = int("0xffff", 16)
End_of_Packet_id = int("0xffff", 16)
Client_id = 250


def build_ack(segment_no):
    return Start_of_Packet_id.to_bytes(2, 'big') + Client_id.to_bytes(1, 'big') + ACK.to_bytes(2, 'big') +\
        segment_no.to_bytes(1, 'big') + End_of_Packet_id.to_bytes(2, 'big')


def build_reject_2(segment_no):
    return Start_of_Packet_id.to_bytes(2, 'big') + Client_id.to_bytes(1, 'big') + REJECT.to_bytes(2, 'big') + \
        REJECT_length_mismatch.to_bytes(2, 'big') + segment_no.to_bytes(1, 'big') + End_of_Packet_id.to_bytes(2, 'big')


def build_reject_1(segment_no):
    return Start_of_Packet_id.to_bytes(2, 'big') + Client_id.to_bytes(1, 'big') + REJECT.to_bytes(2, 'big') + \
        REJECT_out_of_sequence.to_bytes(2, 'big') + segment_no.to_bytes(1, 'big') + End_of_Packet_id.to_bytes(2, 'big')


def build_reject_3(segment_no):
    return Start_of_Packet_id.to_bytes(2, 'big') + Client_id.to_bytes(1, 'big') + REJECT.to_bytes(2, 'big') + \
        REJECT_End_of_packet_missing.to_bytes(2, 'big') + segment_no.to_bytes(1, 'big') + End_of_Packet_id.to_bytes(2, 'big')


def build_reject_4(segment_no):
    return Start_of_Packet_id.to_bytes(2, 'big') + Client_id.to_bytes(1, 'big') + REJECT.to_bytes(2, 'big') + \
        REJECT_Duplicate_packet.to_bytes(2, 'big') + segment_no.to_bytes(1, 'big') + End_of_Packet_id.to_bytes(2, 'big')


# clear and initialize the output file
file = open('output_server.txt', 'w')
file.truncate(0)
now = datetime.now()
file.write("Welcome to my program, now is: " + now.strftime("%H:%M:%S"))
file.write("\n\nServer receives the following messages:\n\n")
file.close()

while True:
    data, addr = server_socket.recvfrom(4096)
    segment_no = data[5]
    payload = data[7:-2].decode()
    length = data[6]
    received_end = data[-2:]
    print(data)

    if received_end != b'\xff\xff':
        # error 3
        print("error 3: End of packet missing")
        rej_msg = build_reject_3(segment_no)
        server_socket.sendto(rej_msg, addr)
        print("reject sent")
    elif len(payload) != length:
        # error 2
        print(f"the received data has length of {len(payload)}, but the noted length is {length}")
        print("error 2: length mismatch")
        rej_msg = build_reject_2(segment_no)
        server_socket.sendto(rej_msg, addr)
        print("reject sent")
    elif seq_num != -1 and seq_num == segment_no:
        # error 4
        print("error 4: duplicate package")
        rej_msg = build_reject_4(segment_no)
        server_socket.sendto(rej_msg, addr)
        print("reject sent")
    elif seq_num != -1 and seq_num + 1 != segment_no:
        # error 1
        print("error 1: out of sequence")
        rej_msg = build_reject_1(segment_no)
        server_socket.sendto(rej_msg, addr)
        print("reject sent")
    else:
        # correct message, should send ACK
        ACK_msg = build_ack(segment_no)
        server_socket.sendto(ACK_msg, addr)
        seq_num = segment_no    # memorize the segment_no of successfully received message
        # write in output file
        file = open('output_server.txt', 'a')
        file.write(payload + "\n")
        file.close()

#server_socket.close()