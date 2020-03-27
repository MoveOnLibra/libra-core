from canoser import DelegateT, Uint8, BytesT
from libra.hasher import gen_hasher, HashValue

import hashlib, random
from datetime import datetime

ADDRESS_LENGTH = 16
HEX_ADDRESS_LENGTH = ADDRESS_LENGTH * 2

class Address(DelegateT):
    delegate_type = BytesT(ADDRESS_LENGTH, encode_len=False)

    LENGTH = ADDRESS_LENGTH

    @classmethod
    def default(cls):
        return b'\x00' * ADDRESS_LENGTH

    @classmethod
    def from_public_key(cls, pubkey):
        return HashValue.from_sha3_256(pubkey)[HashValue.LENGTH-ADDRESS_LENGTH:]

    @classmethod
    def hash(cls, address):
        shazer = gen_hasher(b"AccountAddress::libra_types::account_address")
        shazer.update(address)
        return shazer.digest()

    @classmethod
    def random(cls):
        return bytes([random.randint(0, Uint8.max_value) for x in range(ADDRESS_LENGTH)])

    @staticmethod
    def normalize_to_bytes(address):
        if isinstance(address, str):
            return strict_parse_address(address)
        if isinstance(address, bytes):
            if len(address) != ADDRESS_LENGTH:
                raise ValueError(f"{address} is not a valid address.")
            return address
        if isinstance(address, bytearray):
            if len(address) != ADDRESS_LENGTH:
                raise ValueError(f"{address} is not a valid address.")
            return bytes(address)
        if isinstance(address, list):
            if len(address) != ADDRESS_LENGTH:
                raise ValueError(f"{address} is not a valid address.")
            return bytes(address)
        raise TypeError(f"Address: {address} has unknown type.")


    @staticmethod
    def from_hex_literal(literal):
        from libra.rustlib import ensure, bail
        ensure(literal.startswith("0x"), "literal must start with 0x.")
        bys = literal[2:]
        if len(bys) % 2 != 0:
            bys = bytes.fromhex('0'+bys)
        else:
            bys = bytes.fromhex(bys)

        if len(bys) > ADDRESS_LENGTH:
            bail("The Address {} is of invalid length", literal)
        elif len(bys) < ADDRESS_LENGTH:
            return bys.rjust(ADDRESS_LENGTH, b'\x00')
        else:
            return bys


    @staticmethod
    def equal_address(addr1, addr2):
        return Address.normalize_to_bytes(addr1) == Address.normalize_to_bytes(addr2)


def parse_address(s: str) -> bytes:
    if s[0:2] == '0x':
        s = s[2:]
        if len(s) < HEX_ADDRESS_LENGTH:
            s = s.rjust(HEX_ADDRESS_LENGTH, '0')
    if len(s) == HEX_ADDRESS_LENGTH:
        return bytes.fromhex(s)
    return None

def strict_parse_address(s: str) -> bytes:
    def strict_parse_address(s: str, orig_str: str) -> bytes:
        if len(s) < HEX_ADDRESS_LENGTH:
            raise ValueError(f"{orig_str} is not a valid address.")
        elif len(s) == HEX_ADDRESS_LENGTH:
            return bytes.fromhex(s)
        elif s[0:2] == '0x':
            return strict_parse_address(s[2:], orig_str)
        elif s[0]=="'" and s[-1]=="'":
            return strict_parse_address(s[1:-1], orig_str)
        elif s[0]=='"' and s[-1]=='"':
            return strict_parse_address(s[1:-1], orig_str)
        else:
            raise ValueError(f"{orig_str} is not a valid address.")
    return strict_parse_address(s, s)
