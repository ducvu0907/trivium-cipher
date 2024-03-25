import os
from bitstring import BitArray

class Trivium:
  def __init__(self):
    self.state = None
    self.gen_random_key_iv(80)
    self.loading()
    
  def gen_random_key_iv(self, length):
    self.key = BitArray(bytes=os.urandom(length // 8))
    self.iv = BitArray(bytes=os.urandom(length // 8))

  def loading(self):
    self.state = BitArray(length=288)
    self.state[:80] = self.key
    self.state[93:173] = self.iv
    self.state[281:] = BitArray('0b00000111')
    for _ in range(4 * 288):
      self.gen_keystream()
    
  def gen_keystream(self):
    t1 = self.state[65] ^ self.state[92]
    t2 = self.state[161] ^ self.state[176]
    t3 = self.state[242] ^ self.state[287]
    output_bit = t1 ^ t2 ^ t3
    t1 = t1 ^ (self.state[90] & self.state[91]) ^ self.state[170]
    t2 = t2 ^ (self.state[174] & self.state[175]) ^ self.state[263]
    t3 = t3 ^ (self.state[285] & self.state[286]) ^ self.state[68]
    self.state = self.state >> 1
    self.state[0] = t3
    self.state[93] = t1
    self.state[177] = t2
    return output_bit
  
  def keystream(self, msglen):
    cnt, keystream = 0, []
    while cnt < msglen:
      keystream.append(self.gen_keystream())
      cnt += 1
    return keystream
  
  def encrypt(self, plaintext):
    pass

  def decrypt(self, ciphertext):
    pass
  
# testing
trivium = Trivium()
test_input = BitArray('0b111111111101010101010')
keystream = BitArray(trivium.keystream(len(test_input)))
test_output = test_input.__xor__(keystream)
print(test_output)