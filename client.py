import socket
import firstStep
from datetime import datetime
import time


# connect to server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind(('127.0.0.1', 12345))
data, addr = client_socket.recvfrom(4096)

# global variables: the essential elements of data packet
Start_of_Packet_id = int("0xffff", 16)
Client_id = 250
DATA = int("0xfff1", 16)


def build_data_packets(filename):
    """read five messages that need to be transmitted"""
    with open(filename) as f:
        msg_list = f.readlines()

    packets = []
    # for each line of messages, build an individual data packet
    for msg in msg_list:
        msg_parts = msg.split(", ")
        segment_no = int(msg_parts[0])
        length = int(msg_parts[1], 16)
        payload = msg_parts[2]
        end_of_packet_id= int(msg_parts[3], 16)
        packet = Start_of_Packet_id.to_bytes(2, 'big') + Client_id.to_bytes(1, 'big') + DATA.to_bytes(2, 'big') + \
                 segment_no.to_bytes(1, 'big') + length.to_bytes(1, 'big') + \
                 payload.encode("utf-8") + end_of_packet_id.to_bytes(2, 'big')
        packets.append(packet)

    return packets


def ini_output():
    """clear and initialize the output file"""
    file = open('output_client.txt', 'w')
    file.truncate(0)
    now = datetime.now()
    file.write("Welcome to my program, now is: " + now.strftime("%H:%M:%S"))
    file.write("\n\nClient receives the following responses:\n\n")
    file.close()


def read(response):
    if len(response) == 8:  # success
        sentense = f"ACK for the segment no.{int(response[5])}.\n"
        print(sentense)
        # write in output file
        file = open('output_client.txt', 'a')
        file.write(sentense)
        file.close()
        return True
    else:   #fail
        error_seg_no = int(response[7])
        if response[6] == 244:
            sentense = f"The segment no.{error_seg_no} was rejected because it was out of sequence.\n"
            print(sentense)
            # write in output file
            file = open('output_client.txt', 'a')
            file.write(sentense)
            file.close()
        elif response[6] == 247:
            sentense = f"The segment no.{error_seg_no} was rejected because it was duplicated.\n"
            print(sentense)
            file = open('output_client.txt', 'a')
            file.write(sentense)
            file.close()
        elif response[6] == 245:
            sentense = f"The segment no.{error_seg_no} was rejected because it was mismatched with the length.\n"
            print(sentense)
            file = open('output_client.txt', 'a')
            file.write(sentense)
            file.close()
        else:
            sentense = f"The segment no.{error_seg_no} was rejected because it lost its end of packets.\n"
            print(sentense)
            file = open('output_client.txt', 'a')
            file.write(sentense)
            file.close()


data_packets = build_data_packets(firstStep.fileName)  # build a packets for all messages
ini_output()


for i in range(5):
    attempts = 0
    success = False
    buffer = data_packets[i]
    print(buffer)
    while attempts < 3 and not success:
        attempts += 1
        client_socket.sendto(buffer, addr)
        client_socket.settimeout(3)
        try:
            response, addr = client_socket.recvfrom(4096)
            print(response)
            success = read(response)
        except socket.timeout:
            print(f"(At time {datetime.now()}: No response received, attempt {attempts})\n")
            file = open('output_client.txt', 'a')
            file.write(f"(At time {datetime.now()}: No response received, attempt {attempts})\n")
            file.close()
            continue
    if attempts == 3 and not success:
        print("(Server does not respond.)")
        file = open('output_client.txt', 'a')
        file.write("(Server does not respond.)")
        file.close()
        break