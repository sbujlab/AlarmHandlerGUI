'''
Alarm Handler GUI Revamp
Code Commissioned 2019-01-04
Code by A.J. Zec
Greyed and Alarmed by Cameron
  2019-05-28
'''
import socket
import select
import sys
import os

from ctypes import *

""" This class defines a C-like struct """
class Payload(Structure):
  #_fields_ = [("cbuf", c_char_p*10),("ibuf", c_char_p*12)]
  _fields_ = [("cbuf", c_char*10),("ibuf", c_int*12)]
  # Bob's is a 
  #struct charint {
  #  char cbuf[10];
  #  int ibuf[12];
  #};

class sockClient:

  def __init__(self, addr):
    self.addr = addr

  def sendPacket(self, buff):
    self.server_addr = (self.addr, 5077)
    try: 
      self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM|socket.SOCK_NONBLOCK,0)
      readers, writers, errs = [self.s], [], []
      timeout = 7
      ready_to_read, ready_to_write, in_error = select.select(readers, writers, errs, timeout)
      self.s.setblocking(1)
      #self.s.setblocking(0)
      #print("Socket successfully created")
    except socket.error as err: 
      print("Socket creation failed with error {}".format(err))

    try:
      self.s.connect(self.server_addr)
      #print("Connected to {}".format(repr(self.server_addr)))
    except:
      print("ERROR: Connection to {} refused".format(repr(self.server_addr)))
      sys.exit(1)

    try:
      #print("Sending new packet, data = {}".format(buff))
      payload_out = Payload()
      payload_out.ibuf[0] = int(buff)

      #print("Sending ibuf[0]={}".format(payload_out.ibuf[0]))
      nsent = self.s.send(payload_out)

      # all data has been sent or an error occurs. No return value.
      #print("Sent {} bytes".format(nsent))
      # Hypothetically one would want to know if the server 
      # successfully alarmed or not, but for now just move on
      #buff = self.s.recv(sizeof(Payload))
      #payload_in = Payload.from_buffer_copy(buff)
      #print("Received ibuf[0]={}".format(payload_in.ibuf[0]))
    finally:
      #print("Closing socket")
      self.s.close()
    return "Sent Packet"
