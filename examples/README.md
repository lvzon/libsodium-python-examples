# libsodium-python Examples

To use these examples, you will need to have libsodium installed, and Python should be able to find 
the bindings file `libsodium.py`. 

To install libsodium, follow the [installation guide](https://download.libsodium.org/doc/installation/).
On Ubuntu and other Debian-based Linux systems, you can simply do: `sudo apt-get install libsodium-dev`

For the Python bindings, you can either use [libnacl >=v1.6.0](https://github.com/saltstack/libnacl), 
or you can use the bindings file `libsodium.py`, which is included here.
For python to find a module, it should be in one of the directories listed in `sys.path`, 
so if you use `libsodium.py`, you can copy or link to your current project directory,
install it in your home directory (e.g. for Python 3.5 under: `~/.local/lib/python3.5/site-packages/`) 
or install it system-wide (e.g. for Python 3.5 under: `/usr/local/lib/python3.5/dist-packages/`).

The script `keygen_ed25519.py` can be used to generate an Ed25519 public/private keypair.
For example, the command below will generate `test_pubkey.ed25519` and `test_secret.ed25519`:

```
./keygen_ed25519.py test
```

These keys can be used to generate signed messages, for instance a signed version of this README-file:

```
./sign.py test_secret.ed25519 README.md signed_message
```

If all goes well, you can verify and dump the original message with `verify.py`:

```
./verify.py test_pubkey.ed25519 signed_message
```

You can also just generate and verify a signature:

```
./signature_generate.py test_secret.ed25519 README.md testsignature
./signature_verify.py test_pubkey.ed25519 README.md testsignature
```

To generate a signed and encrypted message, you'll need two keypairs, one for the sender and one for the receiver:

```
./keygen_ed25519.py client
./keygen_ed25519.py server
```

To encrypt a message, use the private key of the sender and the public key of the receiver:

```
./encrypt_ed25519.py client_secret.ed25519 server_pubkey.ed25519 README.md encrypted_message
```

To authenticate and decrypt the message, you'll need the public key of the sender and the private key of the receiver:

```
./decrypt_ed25519.py server_secret.ed25519 client_pubkey.ed25519 encrypted_message
```

August 2017, Levien van Zon (https://github.com/lvzon)

