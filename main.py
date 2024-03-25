import os
from bitstring import BitArray

class Trivium:
  def __init__(self, key, iv):
    self.state = BitArray(length=288)
    self.key = BitArray(bytes=key)
    self.iv = BitArray(bytes=iv)
    
  def loading(self):
    self.state[:80] = self.key
    self.state[93:173] = self.iv
    self.state[281:] = BitArray('0b00000111')
    for _ in range(1152):
      self.clock()
    
  def clock(self):
    pass