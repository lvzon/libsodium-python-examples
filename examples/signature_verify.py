#!/usr/bin/python3

import sys
import libsodium

def write_bytes(fname, data):
    with open(fname, 'wb') as outfile:
        outfile.write(data)
    
def read_bytes(fname):
    with open(fname, 'rb') as infile:
        data = infile.read()
    return data

# Get input/output files from commandline

if len(sys.argv) < 3 or sys.argv[1] in ('-h', '--help'):
    print("Usage:", sys.argv[0], "<ed25519 sender pubkey> <input message file> [<input signature file>]\n")
    exit()


# Load Ed25519 keyfile

sender_pubkey_ed25519 = read_bytes(sys.argv[1])

# Read message to be verified

message = read_bytes(sys.argv[2])

# Read signature to be verified
    
if len(sys.argv) >= 4:
    signature = read_bytes(sys.argv[3])
else:
    signature = sys.stdin.buffer.read()

# Verify signature

try:
    libsodium.crypto_sign_verify_detached(signature, message, sender_pubkey_ed25519)
except:
    print("Signature does not match message\n")
    exit(1)

print("Signature matches message\n")
