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

# Get prefix from commandline

prefix = ''
lastchar = ''

if len(sys.argv) > 1:
    prefix = sys.argv[1]
    lastchar = prefix[-1]

# Add underscore if needed

if lastchar and lastchar not in ('/', '\\', '.', '-', '_'):
    prefix += '_'

# Generate Ed25519 keypair, write to files

pubkey, secret = libsodium.crypto_sign_ed25519_keypair()
write_bytes(prefix + "pubkey.ed25519", pubkey)
write_bytes(prefix + "secret.ed25519", secret)

# For more information, see: https://download.libsodium.org/doc/advanced/ed25519-curve25519.html
# Note that an Ed25519 keypair can be used for signatures and can be converted into a 
# Curve25519 keypair for authenticated encryption, but if you only need authenticated encryption 
# you should simply generate a Curve25519-keypair and use that.
