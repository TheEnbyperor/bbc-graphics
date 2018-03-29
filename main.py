import socket

TCP_IP = '172.30.0.15'
TCP_PORT = 23
BUFFER_SIZE = 128

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

commands = {
    0x12: ("GCOL", 2),
    0x13: ("LCOL", 5),
    0x19: ("PLOT", 5),
    0x1d: ("ORGIN", 4)
}

isInCommand = False
curCommand = None
gotCommandBytes = 0
curCommandBytes = []

while True:
    data = s.recv(BUFFER_SIZE)

    if data != b'':
        for b in data:
            if isInCommand:
                if gotCommandBytes != commands[curCommand][1]:
                    curCommandBytes.append(b)
                    gotCommandBytes += 1
                elif gotCommandBytes == commands[curCommand][1]:
                    print("{}, {}".format(commands[curCommand][0], curCommandBytes))

                    isInCommand = False
                    gotCommandBytes = 0
                    curCommandBytes = []
                    curCommand = None
            if not isInCommand:
                if b in commands:
                    isInCommand = True
                    curCommand = b


