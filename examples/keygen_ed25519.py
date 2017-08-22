#!/usr/bin/python3

import sys
import libsodium


def write_bytes(fname, data):
    '''
    Write bytes-object to a file
    '''
    with open(fname, 'wb') as outfile:
        outfile.write(data)


def write_bytes_private(fname, data):
    '''
    Write bytes-object to a file that is only readable by the current user
    See: https://stackoverflow.com/questions/5624359/write-file-with-specific-permissions-in-python
    '''
    import os
    import stat
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL  # Refer to "man 2 open".
    mode = stat.S_IRUSR | stat.S_IWUSR  # This is 0o600 in octal and 384 in decimal.
    if os.path.isfile(fname):
        os.remove(fname)
    original_umask = os.umask(0o177)  # 0o777 ^ 0o600
    try:
        fdesc = os.open(fname, flags, mode)
    finally:
        os.umask(original_umask)
    with os.fdopen(fdesc, 'wb') as outfile:
        outfile.write(data)

        
def read_bytes(fname):
    '''
    Read data from file into a bytes-object
    '''
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
write_bytes_private(prefix + "secret.ed25519", secret)

# For more information, see: https://download.libsodium.org/doc/advanced/ed25519-curve25519.html
# Note that an Ed25519 keypair can be used for signatures and can be converted into a 
# Curve25519 keypair for authenticated encryption, but if you only need authenticated encryption 
# you should simply generate a Curve25519-keypair and use that.
