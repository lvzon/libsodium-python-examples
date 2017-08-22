# libsodium-python

Bindings and examples for using low-level libsodium functionality in Python.

The ctype-bindings here are a slightly extended version of [libnacl](https://github.com/saltstack/libnacl)'s 
[`__init__.py`](https://github.com/saltstack/libnacl/blob/master/libnacl/__init__.py), written by 
[Thomas S Hatch](https://github.com/thatch45) and others. See https://github.com/saltstack/libnacl for
the original source code and higher-level bindings for Python.

[Libsodium](https://download.libsodium.org/doc) is a modern C-library for encryption, decryption, signatures, 
password hashing and more, based on the algorithms in Daniel J. Bernstein's [NaCl](http://nacl.cr.yp.to/). 
While there are several interfaces to libsodium for Python, none seemed to provide access to libsodium's
crypto_box_easy-functions (which differ from the NaCl crypto_box-functions in their use of padding bytes).
Because I needed to interface with a C-application that uses 
[crypto_box_easy](https://download.libsodium.org/doc/public-key_cryptography/authenticated_encryption.html), 
I provided bindings to these functions, and to a few other functions specific to libsodium, including:
   - [Conversion of Ed25519 keypairs to Curve25519](https://download.libsodium.org/doc/advanced/ed25519-curve25519.html)
   - Generating keys from seed, and generating public keys from private keys.
   - [Detached signatures and verification](https://download.libsodium.org/doc/public-key_cryptography/public-key_signatures.html)

I have added some [Python-examples](https://github.com/lvzon/libsodium-python/tree/master/examples) on how to use these 
functions to generate an Ed25519 keypair, to derive Curve25519 keys and use these to encrypt a message, and to decrypt 
an encrypted message (which consists of nonce and cipthertext).

To use the examples, you will need to have libsodium installed. 
See the [installation guide](https://download.libsodium.org/doc/installation/) for more information.
On Ubuntu and other Debian-based Linux systems, you can simply do: `sudo apt-get install libsodium-dev`

