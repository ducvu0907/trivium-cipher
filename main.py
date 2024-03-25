import os
from bitstring import BitArray

class Trivium:
  def __init__(self, key, iv):
    self.state = None
    self.key = key
    self.iv = iv
    self.keystream = []
    self.gen_key_iv(80)
    self.loading()
    
  def gen_key_iv(self, length):
    self.key = BitArray(bytes=os.urandom(length // 8))
    self.iv = BitArray(bytes=os.urandom(length // 8))

  def loading(self):
    self.state = BitArray(length=288)
    self.state[:80] = self.key
    self.state[93:173] = self.iv
    self.state[281:] = BitArray('0b00000111')
    for _ in range(4 * 288):
      self.keystream.append(self.clocking())
    
  def clocking(self):
    t1 = self.state[65] ^ self.state[92]
    t2 = self.state[161] ^ self.state[176]
    t3 = self.state[242] ^ self.state[287]
    output_bit = t1 ^ t2 ^ t3
    t1 = t1 ^ (self.state[90] ^ self.state[91]) ^ self.state[170]
    t2 = t2 ^ (self.state[174] ^ self.state[175]) ^ self.state[264]
    t3 = t3 ^ (self.state[285] ^ self.state[286]) ^ self.state[68]
    self.state = self.state >> 1
    self.state[0] = t3
    self.state[93] = t1
    self.state[177] = t2
    return output_bit