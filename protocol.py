'''
Module to define the protocol shared between client/server
based on Professor Dr. Hao Wu's implementation
'''

# Headers

REQ_LIST = "RL"  # client requested list of files
REQ_FILE = "RF"  # client requesting a file
SAVE_FILE = "FD"  # server is sending file client needs to save it
SEND_LIST = "SL"  # server sending the list
ERR = "ER"  # something went wrong (becase of tcp this should not happen)
# kills the server/client. This is testing only and would not be in production.
KILL_SERVER = 'KS'


def prep_send(header, msg):
    return (header+msg).encode()


# Takes in a header and a list of files to be transfered and converts them to a csv string
def prep_list(header, file_list):
    msg = header
    for i in range(len(file_list)):
        if (i == len(file_list)-1):
            msg += file_list[i]
        else:
            msg += file_list[i] + ","
    return(msg.encode())


def decode_incoming(msg):
    if(len(msg) <= 2):
        return(ERR, "EMPTY MESSAGE")
    else:
        return(msg[0:2], msg[2:])
