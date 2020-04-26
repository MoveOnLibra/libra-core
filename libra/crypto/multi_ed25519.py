from __future__ import annotations
from libra.crypto.ed25519 import (
    Ed25519PrivateKey, Ed25519PublicKey, Ed25519Signature, ED25519_PRIVATE_KEY_LENGTH,
    ED25519_PUBLIC_KEY_LENGTH, ED25519_SIGNATURE_LENGTH,
    _generate_keypair_by_private_key
)
from libra.hasher import HashValue
from canoser import Uint8, Uint32, Struct, bytes_to_int_list
from libra.rustlib import flatten, usize
from typing import List, Tuple, Optional
from nacl.signing import VerifyKey


class CryptoMaterialError(Exception):
    def __init__(self, t: str, message: str = None):
        self.t = t
        self.message = message

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

    # Construct a new MultiEd25519PrivateKey.
    @classmethod
    def new(cls,
            private_keys: List[Ed25519PrivateKey],
            threshold: Uint8,
            ) -> MultiEd25519PrivateKey:
        num_of_keys = private_keys.__len__()
        if threshold == 0 or num_of_keys < threshold:
            raise CryptoMaterialError('ValidationError')
        elif num_of_keys > MAX_NUM_OF_KEYS:
            raise CryptoMaterialError('WrongLengthError')
        else:
            return MultiEd25519PrivateKey(
                private_keys,
                threshold,
            )

    # Convenient method to create a MultiEd25519PrivateKey from a single Ed25519PrivateKey.
    def fromEd25519PrivateKey(ed_private_key: Ed25519PrivateKey) -> MultiEd25519PrivateKey:
        return MultiEd25519PrivateKey([ed_private_key], 1)

    # Sign a message with the minimum amount of keys to meet threshold (starting from left-most keys).

    def sign_message(self, message: HashValue) -> MultiEd25519Signature:
        signatures: List[Ed25519Signature] = []
        bitmap = [0] * BITMAP_NUM_OF_BYTES
        for (i, item) in enumerate(self.private_keys[0:self.threshold]):
            bitmap_set_bit(bitmap, i)
            signatures.append(item.sign_message(message))

        return MultiEd25519Signature(signatures, bitmap)

    def length(self) -> usize:
        self.private_keys.__len__() * ED25519_PRIVATE_KEY_LENGTH + 1

    @classmethod
    def genesis(cls) -> MultiEd25519PrivateKey:
        buf = [0] * ED25519_PRIVATE_KEY_LENGTH
        buf[ED25519_PRIVATE_KEY_LENGTH - 1] = 1
        return MultiEd25519PrivateKey(
            private_keys=[bytes(buf)],
            threshold=1,
        )


# Vector of public keys in the multi-key Ed25519 structure along with the threshold.
class MultiEd25519PublicKey(Struct):
    _fields = [
        ('public_keys', [Ed25519PublicKey]),
        ('threshold', Uint8)
    ]

    @classmethod
    def encode(cls, obj):
        output = b''
        for key in obj.public_keys:
            output += key
        output += Uint8.encode(obj.threshold)
        return Uint32.serialize_uint32_as_uleb128(len(output)) + output

    @classmethod
    def decode(cls, cursor):
        buffer_size = Uint32.parse_uint32_from_uleb128(cursor)
        buffer = cursor.buffer[cursor.offset: cursor.offset+buffer_size]
        size = (buffer_size - 1) // ED25519_PUBLIC_KEY_LENGTH
        assert (buffer_size - 1) % ED25519_PUBLIC_KEY_LENGTH == 0
        public_keys = []
        for i in range(size):
            key = buffer[i*ED25519_PUBLIC_KEY_LENGTH:(i+1)*ED25519_PUBLIC_KEY_LENGTH]
            public_keys.append(key)
        threshold = buffer[-1]
        cursor.offset += buffer_size
        return cls(public_keys, threshold)


    # Construct a new MultiEd25519PublicKey.
    # --- Rules ---
    # a) threshold cannot be zero.
    # b) public_keys.__len__() should be equal to or larger than threshold.
    # c) support up to MAX_NUM_OF_KEYS public keys.

    def new(
        public_keys: List[Ed25519PublicKey],
        threshold: Uint8,
    ) -> MultiEd25519PublicKey:
        num_of_keys = public_keys.__len__()
        # TODO: check the same rules when deserialize
        if threshold == 0 or num_of_keys < threshold:
            raise CryptoMaterialError('ValidationError')
        elif num_of_keys > MAX_NUM_OF_KEYS:
            raise CryptoMaterialError('WrongLengthError')
        else:
            return MultiEd25519PublicKey(
                public_keys,
                threshold,
            )

    # Convenient method to create a MultiEd25519PublicKey from a single Ed25519PublicKey.
    @classmethod
    def fromEd25519PublicKey(cls, ed_public_key: Ed25519PublicKey) -> MultiEd25519PublicKey:
        return MultiEd25519PublicKey(
            public_keys=[ed_public_key],
            threshold=1,
        )

    @classmethod
    def fromMultiEd25519PrivateKey(cls, private_key: MultiEd25519PrivateKey) -> MultiEd25519PublicKey:
        public_keys = [_generate_keypair_by_private_key(x)[1] for x in private_key.private_keys]
        return MultiEd25519PublicKey(
            public_keys,
            private_key.threshold,
        )

    def length(self) -> usize:
        self.public_keys.__len__() * ED25519_PUBLIC_KEY_LENGTH + 1


# Vector of the multi-key signatures along with a 32bit [Uint8; 4] bitmap required to map signatures
# with their corresponding public keys.
#
# Note that bits are read from left to right. For instance, in the following bitmap
# [0b0001_0000, 0b0000_0000, 0b0000_0000, 0b0000_0001], the 3rd and 31st positions are set.
class MultiEd25519Signature(Struct):
    _fields = [
        ('signatures', [Ed25519Signature]),
        ('bitmap', [Uint8, BITMAP_NUM_OF_BYTES])
    ]

    @classmethod
    def encode(cls, obj):
        output = b''
        for key in obj.signatures:
            output += key
        output += bytes(obj.bitmap)
        return Uint32.serialize_uint32_as_uleb128(len(output)) + output

    @classmethod
    def decode(cls, cursor):
        buffer_size = Uint32.parse_uint32_from_uleb128(cursor)
        buffer = cursor.buffer[cursor.offset: cursor.offset+buffer_size]
        size = (buffer_size - 4) // ED25519_SIGNATURE_LENGTH
        assert (buffer_size - 4) % ED25519_SIGNATURE_LENGTH == 0
        signatures = []
        for i in range(size):
            key = buffer[i*ED25519_SIGNATURE_LENGTH:(i+1)*ED25519_SIGNATURE_LENGTH]
            signatures.append(key)
        bitmap = bytes_to_int_list(buffer[-4:])
        cursor.offset += buffer_size
        return cls(signatures, bitmap)



    # This method will also sort signatures based on index.
    @classmethod
    def new(cls,
            signatures: List[Tuple[Ed25519Signature, Uint8]],
            ) -> MultiEd25519Signature:
        num_of_sigs = signatures.__len__()
        if num_of_sigs == 0 or num_of_sigs > MAX_NUM_OF_KEYS:
            raise CryptoMaterialError('ValidationError')

        sorted_signatures = signatures.sort(key=lambda x: x[1])
        bitmap = [0] * BITMAP_NUM_OF_BYTES

        # Check if all indexes are unique and < MAX_NUM_OF_KEYS
        sigs = [x[0] for x in sorted_signatures]
        indexes = [x[1] for x in sorted_signatures]

        for i in indexes:
            # If an index is out of range.
            if i < MAX_NUM_OF_KEYS:
                # if an index has been set already (thus, there is a duplicate).
                if bitmap_get_bit(bitmap, i):
                    raise CryptoMaterialError('BitVecError',
                                              "Duplicate signature index",
                                              )
                else:
                    bitmap_set_bit(bitmap, i)
            else:
                raise CryptoMaterialError('BitVecError',
                                          "Signature index is out of range",
                                          )

        return MultiEd25519Signature(sigs, bitmap)

    # Serialize a MultiEd25519Signature in the form of sig0||sig1||..sigN||bitmap.

    def to_bytes(self) -> bytes:
        pass  # TODO: why not use lcs
        # bytes: List[Uint8] = self
        #     .signatures
        #     .iter()
        #     .flat_map(|sig| sig.to_bytes())
        #     .collect()
        # bytes.extend(self.bitmap[..])

    def length(self) -> usize:
        return self.signatures.__len__() * ED25519_SIGNATURE_LENGTH + BITMAP_NUM_OF_BYTES

    # Checks that `self` is valid for `message` using `public_key`.

    def verify(self, message: HashValue, public_key: MultiEd25519PublicKey) -> None:
        self.verify_arbitrary_msg(message, public_key)

    # Checks that `self` is valid for an arbitrary bytes `message` using `public_key`.
    # Outside of this crate, this particular function should only be used for native signature
    # verification in Move.

    def verify_arbitrary_msg(
        self,
        message: bytes,
        public_key: MultiEd25519PublicKey,
    ) -> None:
        last_bit = bitmap_last_set_bit(self.bitmap)
        if last_bit == None or last_bit > public_key.length():
            raise CryptoMaterialError('BitVecError', "Signature index is out of range")

        if bitmap_count_ones(self.bitmap) < public_key.threshold:
            raise CryptoMaterialError('BitVecError',
                                      "Not enough signatures to meet the threshold"
                                      )

        bitmap_index = 0
        # TODO use deterministic batch verification when gets available.
        for sig in self.signatures:
            while not bitmap_get_bit(self.bitmap, bitmap_index):
                bitmap_index += 1
            pk = public_key.public_keys[bitmap_index]
            pk = VerifyKey(bytes(public_key.public_keys[bitmap_index]))
            pk.verify(message, sig)
            bitmap_index += 1

    @classmethod
    def fromEd25519Signature(cls, ed_signature: Ed25519Signature) -> MultiEd25519Signature:
        return MultiEd25519Signature(
            [ed_signature],
            # "1000_0000 0000_0000 0000_0000 0000_0000"
            [0b1000_0000, 0, 0, 0],
        )


def bitmap_set_bit(bitmap: List[Uint8], index: usize):
    bucket = index // 8
    # It's always invoked with index < 32, thus there is no need to check range.
    bucket_pos = index - (bucket * 8)
    bitmap[bucket] |= 128 >> bucket_pos


# Helper method to get the input's bit at index.
def bitmap_get_bit(bitmap: List[Uint8], index: usize) -> bool:
    bucket = index // 8
    # It's always invoked with index < 32, thus there is no need to check range.
    bucket_pos = index - (bucket * 8)
    return (bitmap[bucket] & (128 >> bucket_pos)) != 0


# Returns the number of set bits.
def bitmap_count_ones(bitmap: List[Uint8]) -> Uint32:
    bitvec = flatten([bin(x)[2:].rjust(8, '0') for x in bitmap])
    ret = 0
    for (i, bit) in enumerate(bitvec):
        if bit == '1':
            ret += 1
    return ret

# Find the last set bit.


def bitmap_last_set_bit(bitmap: List[Uint8]) -> Optional[Uint8]:
    bitvec = flatten([bin(x)[2:].rjust(8, '0') for x in bitmap])
    ret = None
    for (i, bit) in enumerate(bitvec):
        if bit == '1':
            ret = i
    return ret
