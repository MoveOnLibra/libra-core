from __future__ import annotations
from libra.account_address import Address
from libra.crypto.ed25519 import Ed25519PublicKey, Ed25519Signature
from libra.crypto.multi_ed25519 import MultiEd25519PublicKey, MultiEd25519Signature
from libra.hasher import HashValue
from libra.rustlib import ensure
from canoser import Uint8, Struct, RustEnum
from enum import IntEnum
from nacl.signing import VerifyKey


# A `TransactionAuthenticator` is an an abstraction of a signature scheme. It must know:
# (1) How to check its signature against a message and public key
# (2) How to convert its public key into an `AuthenticationKeyPreimage` structured as
# (public_key | signaure_scheme_id).
# Each on-chain `LibraAccount` must store an `AuthenticationKey` (computed via a sha3 hash of an
# `AuthenticationKeyPreimage`).
# Each transaction submitted to the Libra blockchain contains a `TransactionAuthenticator`. During
# transaction execution, the executor will check if the `TransactionAuthenticator`'s signature on
# the transaction hash is well-formed (1) and whether the sha3 hash of the
# `TransactionAuthenticator`'s `AuthenticationKeyPreimage` matches the `AuthenticationKey` stored
# under the transaction's sender account address (2).



class Scheme(IntEnum):
    Ed25519 = 0
    MultiEd25519 = 1
    # ... add more schemes here

class Ed25519_(Struct):
    _fields = [
        ('public_key', Ed25519PublicKey),
        ('signature', Ed25519Signature)
    ]

class MultiEd25519_(Struct):
    # Single signature
    _fields = [
        ('public_key', MultiEd25519PublicKey),
        ('signature', MultiEd25519Signature)
    ]

class TransactionAuthenticator(RustEnum):
    # K-of-N multisignature
    _enums = [
        ('Ed25519', Ed25519_),
        ('MultiEd25519', MultiEd25519_)
    ]


    def scheme(self) -> Scheme:
        if self.Ed25519:
            return Scheme.Ed25519
        elif self.MultiEd25519:
            return Scheme.MultiEd25519
        else:
            raise AssertsionError("unreachable!")


    # Create a single-signature ed25519 authenticator
    @classmethod
    def ed25519(cls, public_key: Ed25519PublicKey, signature: Ed25519Signature) -> TransactionAuthenticator:
        return cls('Ed25519', Ed25519_(
            public_key,
            signature,
        ))


    # Create a multisignature ed25519 authenticator
    @classmethod
    def multi_ed25519(cls,
        public_key: MultiEd25519PublicKey,
        signature: MultiEd25519Signature,
    ) -> TransactionAuthenticator:
        return cls('MultiEd25519', MultiEd25519_(
            public_key,
            signature,
        ))


    # Return Ok if the authenticator's public key matches its signature, Err otherwise
    def verify_signature(self, message: HashValue) -> None:
        if self.Ed25519:
            vkey = VerifyKey(self.value.public_key)
            vkey.verify(message, self.value.signature)
        elif self.MultiEd25519:
            self.value.signature.verify(message, self.value.public_key)
        else:
            raise AssertsionError("unreachable!")


    # Return the raw bytes of `self.public_key`
    def public_key_bytes(self) -> bytes:
        return self.value.public_key

    # Return the raw bytes of `self.signature`
    def signature_bytes(self) -> bytes:
        return self.value.signature

    # Return an authentication key preimage derived from `self`'s public key and scheme id
    def authentication_key_preimage(self) -> AuthenticationKeyPreimage:
        return AuthenticationKeyPreimage.new(self.public_key_bytes(), self.scheme())


    # Return an authentication key derived from `self`'s public key and scheme id
    def authentication_key(self) -> AuthenticationKey:
        return AuthenticationKey.from_preimage(self.authentication_key_preimage())


    def __str__(self):
        return "TransactionAuthenticator[scheme id: {}, public key: {}, signature: {}]".format(
            self.scheme(),
            self.public_key_bytes().hex(),
            self.signature_bytes().hex(),
        )


# A struct that represents an account authentication key. An account's address is the last 16
# bytes of authentication key used to create it
class AuthenticationKey(bytes):

    # The number of bytes in an authentication key.
    LENGTH = 32

    @classmethod
    def new(cls, bs: bytes) -> AuthenticationKey:
        assert len(bs) == AuthenticationKey.LENGTH
        return cls(bs)

    @classmethod
    def try_from(cls, bs: Union[bytes, str]) -> AuthenticationKey:
        if isinstance(bs, str):
            bs = bytes.fromhex(bs)

        ensure(
            bs.__len__() == AuthenticationKey.LENGTH,
            "The authentication key {} is of invalid length",
            bs
        )
        return cls(bs)


    # Create an authentication key from a preimage by taking its sha3 hash
    @classmethod
    def from_preimage(cls, preimage: AuthenticationKeyPreimage) -> AuthenticationKey:
        return AuthenticationKey.new(HashValue.from_sha3_256(preimage))


    # Create an authentication key from an Ed25519 public key
    @classmethod
    def ed25519(cls, public_key: Ed25519PublicKey) -> AuthenticationKey:
        return cls.from_preimage(AuthenticationKeyPreimage.ed25519(public_key))


    # Create an authentication key from a MultiEd25519 public key
    @classmethod
    def multi_ed25519(cls, public_key: MultiEd25519PublicKey) -> AuthenticationKey:
        return cls.from_preimage(AuthenticationKeyPreimage.multi_ed25519(public_key))


    # Return an address derived from the last `Address.LENGTH` bytes of this
    # authentication key.
    def derived_address(self) -> Address:
        # keep only last 16 bytes
        return self[AuthenticationKey.LENGTH - Address.LENGTH:]


    # Return the first Address.LENGTH bytes of this authentication key
    def prefix(self) -> bytes:
        return self[:Address.LENGTH]


    # Return an abbreviated representation of this authentication key
    def short_str(self) -> str:
        return self[:4].hex()


    # Create a random authentication key. For testing only
    @classmethod
    def random(cls) -> AuthenticationKey:
        from random import randint
        return bytes([randint(0, Uint8.max_value) for x in range(AuthenticationKey.LENGTH)])


# A value that can be hashed to produce an authentication key
class AuthenticationKeyPreimage(bytes):

    # Return bytes for (public_key | scheme_id)
    @classmethod
    def new(cls, public_key_bytes: bytes, scheme: Scheme) -> AuthenticationKeyPreimage:
        return cls(public_key_bytes + scheme.to_bytes(1, byteorder="big"))


    # Construct a preimage from an Ed25519 public key
    @classmethod
    def ed25519(cls, public_key: Ed25519PublicKey) -> AuthenticationKeyPreimage:
        return cls.new(public_key, Scheme.Ed25519)


    # Construct a preimage from a MultiEd25519 public key
    @classmethod
    def multi_ed25519(cls, public_key: MultiEd25519PublicKey) -> AuthenticationKeyPreimage:
        return cls.new(public_key, Scheme.MultiEd25519)
