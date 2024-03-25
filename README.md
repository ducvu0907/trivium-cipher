# Trivium encryption

This is a simple trivium implementation using python
Each file in the test_data folder has been encrypted and stored in the encrypted_data folder
The time was tracked for each file and logged to report.txt for references

# Implementation

1. Initialize random key and IV with the length of 80 bits.
2. Load key to the first 80 bits of shift register A, IV to the first 80 bits of shift register B and constants to the end of shift register C.
3. Execute 1152 rounds of trivium
4. Each bit of the next round will be append to the keystream, so we can just loop an amount of times equal to the length of the input file.
5. Lastly, plaintext and ciphertext are XOR-ed with the keystream for encryption and decryption
