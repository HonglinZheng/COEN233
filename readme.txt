Welcome to my customized UDP implementation!

Before you run any program, please go to the firstStep.py to uncomment one input file.
Read all the instructions in firstStep.py, so you will know how to start my program.


Client is going to send five messages to server.
Server will reply ACK (acknowledge) if the message is correct, yet reply reject if the message is wrong.
Client will retransmit a message once received reject or didn't receive any reply after 3 seconds since sending it.
Client only send and resend any message up to three times.

You can see how client uses timer to deal with no ACK before the timeout by running silentServer.py.
silentServer.py can only builds connection with client.py but never ever reply.

The third line in input_wrong1.txt is wrong as the segment no.22 has wrong information of length.
The fourth line in input_wrong2.txt is wrong as the segment no.17 has wrong end of packet id.
The fifth line in input_wrong3.txt is wrong as the segment no.80 should not follow segment no.77.
The second line in input_wrong4.txt is wrong as the segment no.14 should not repeat.

The input_correct.txt have five correct messages:
    This is Monday / Tuesday is nicer / Wednesday is sunny / Thursday is warm / My favorite day is Friday


I used PyCharm 2022.3.2 to run the program and import three modules: socket, datetime, time.

Honglin