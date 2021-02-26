############################################
# a multicast client, this was developed to 
# experiment with multicast. OpenCv & Socket are
# used to stream video from webcam.
# Athor: Amir Gasmi <argasmi@gmail.com>




import socket
import time
import cv2

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007
# regarding socket.IP_MULTICAST_TTL
# ---------------------------------
# for all packets sent, after two hops on the network the packet will not 
# be re-sent/broadcast (see https://www.tldp.org/HOWTO/Multicast-HOWTO-6.html)
MULTICAST_TTL = 2
vid = cv2.VideoCapture(0) 
string = ' this is a big sentence:\r\n \
 more \
 and even more,\
 and more and more\
 and more and more\
 and more and more\
 and more and more\
 and more and more\
 and more and more\
 and more and more\
 and more and more\
 and more and more\
 and more and more\
 and more and more\r\n\
 end'
CHUNK = 1024
strbytes = string.encode('ASCII')
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

# For Python 3, change next line to 'sock.sendto(b"robot", ...' to avoid the
# "bytes-like object is required" msg (https://stackoverflow.com/a/42612820)
while True:
    ret,frame = vid.read()
    bytedata = frame.tobytes()
    size = len(bytedata)
    i = 1024
    
    while (size > 0):
        sock.sendto(bytedata[i-CHUNK:i], (MCAST_GRP, MCAST_PORT))
        i = i + CHUNK
        size = size - CHUNK
        
    #time.sleep(0.1)