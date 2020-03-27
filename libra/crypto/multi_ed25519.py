from __future__ import annotations
from libra.crypto.ed25519 import (
    Ed25519PrivateKey, Ed25519PublicKey, Ed25519Signature, ED25519_PRIVATE_KEY_LENGTH,
    ED25519_PUBLIC_KEY_LENGTH, ED25519_SIGNATURE_LENGTH
)
from libra.hasher import HashValue
from canoser import Uint8, Uint32, Struct

# This module provides an API for the accountable threshold multi-sig PureEdDSA signature scheme
# over the ed25519 twisted Edwards curve as defined in [RFC8032](https://tools.ietf.org/html/rfc8032).
#
# Signature verification also checks and rejects non-canonical signatures.

# from libra_crypto_derive.{DeserializeKey, SerializeKey, SilentDebug, SilentDisplay}

MAX_NUM_OF_KEYS = 32
BITMAP_NUM_OF_BYTES = 4

# Vector of private keys in the multi-key Ed25519 structure along with the threshold.
class MultiEd25519PrivateKey(Struct):
    _fields = [
        ('private_keys', [Ed25519PrivateKey]),
        ('threshold', Uint8)
    ]

# Vector of public keys in the multi-key Ed25519 structure along with the threshold.
class MultiEd25519PublicKey(Struct):
    _fields = [
        ('public_keys', [Ed25519PublicKey]),
        ('threshold', Uint8)
    ]

# Vector of the multi-key signatures along with a 32bit [Uint8; 4] bitmap required to map signatures
# with their corresponding public keys.
#
# Note that bits are read from left to right. For instance, in the following bitmap
# [0b0001_0000, 0b0000_0000, 0b0000_0000, 0b0000_0001], the 3rd and 31st positions are set.
class MultiEd25519Signature(Struct):
    _fields = [
        ('signatures', [Ed25519Signature]),
        ('bitmap', bytes) #[Uint8; BITMAP_NUM_OF_BYTES]
    ]

    def verify(self, message: HashValue, public_key: MultiEd25519PublicKey):
        bail("unimplemented!")
