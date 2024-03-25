import os
from bitstring import BitArray
import binascii

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

# encrypt
trivium = Trivium()

def encrypt(plaintext):
  keystream = BitArray(trivium.keystream(len(plaintext)))
  return keystream ^ plaintext

def decrypt(ciphertext):
  keystream = BitArray(trivium.keystream(len(ciphertext)))
  return keystream ^ ciphertext

def file_to_binary_string(file_path):
  with open(file_path, 'rb') as file:
    binary_code = file.read()  
  return BitArray(bytes=binary_code)

def process_dir(dir):
  for filename in os.listdir(dir):
    f = os.path.join(dir, filename)
    if os.path.isfile(f):
      pass

if __name__ == '__main__':
  bin_str = file_to_binary_string('test_data/ptt5')
  keystream = BitArray(trivium.keystream(len(bin_str)))
  with open('encrypted_data/ptt5.txt', 'w') as file:
    file.write(keystream.__xor__(bin_str).bin)