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
    print("Usage:", sys.argv[0], "<ed25519 sender secret> [<input file> [<output signature file>]]\n")
    exit()


# Load Ed25519 keyfile

sender_secret_ed25519 = read_bytes(sys.argv[1])

# Read message to be signed (from file or stdin)

if len(sys.argv) >= 3:
    message = read_bytes(sys.argv[2])
else:
    message = sys.stdin.buffer.read()
    

# Generate signature and write to output

signature = libsodium.crypto_sign_detached(message, sender_secret_ed25519)


if len(sys.argv) >= 4:
    write_bytes(sys.argv[3], signature)
else:
    sys.stdout.buffer.write(signature)
