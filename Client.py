############################################
# a multicast client, this was developed to 
# experiment with multicast. OpenCv & Socket are
# used to stream video from webcam.
# Athor: Amir Gasmi <argasmi@gmail.com>

import socket
import struct
import cv2
import numpy as np



MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007
IS_ALL_GROUPS = True

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if IS_ALL_GROUPS:
    # on this port, receives ALL multicast groups
    sock.bind(('', MCAST_PORT))
else:
    # on this port, listen ONLY to MCAST_GRP
    sock.bind((MCAST_GRP, MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
sync = True
buffer_size = 1024
while True:
    frame_size = 921600
    databyte = b""
  # For Python 3, change next line to "print(sock.recv(10240))"
    while(frame_size >0):
        buf = sock.recv(buffer_size)
        if(sync ):
            if(len(buf) < buffer_size):
                sync = True
                break
        
        databyte = b"".join([databyte,buf])
        frame_size = frame_size -buffer_size
        
    data = np.frombuffer(databyte, dtype=np.uint8)
    frame_matrix = np.array(data)
    frame_matrix = np.reshape(frame_matrix, (480, 640,3))
    cv2.imshow("Video Stream",frame_matrix)
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
  
# After the loop release the cap object 

# Destroy all the windows 
cv2.destroyAllWindows() 
    