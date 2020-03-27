from nacl.signing import SigningKey
from libra.hasher import new_sha3_256
from enum import Enum
from libra.account_config import AccountConfig
from libra.account_address import Address
from libra.transaction.authenticator import AuthenticationKey
import libra
import os

AccountStatus = Enum('AccountStatus', ('Local','Persisted','Unknown'))

class Account:
    def __init__(self, private_key, address=None, sequence_number=0):
        self._signing_key = SigningKey(private_key)
        self._verify_key = self._signing_key.verify_key
        if address is None:
            self.gen_address_from_pk(self._verify_key.encode())
        else:
            self.address = Address.normalize_to_bytes(address)
        self.sequence_number = sequence_number
        self.status = AccountStatus.Local

    def gen_address_from_pk(self, public_key):
        auth_key = AuthenticationKey.ed25519(public_key)
        self.auth_key_prefix = auth_key.prefix()
        self.address = auth_key.derived_address()

    def json_print_fields(self):
        return ["address", "private_key", "public_key"]

    @classmethod
    def faucet_account(cls, private_key):
        return cls(private_key, AccountConfig.association_address())

    @classmethod
    def gen_faucet_account(cls, faucet_account_file):
        if faucet_account_file is None:
            faucet_account_file = cls.faucet_file_path()
        with open(faucet_account_file, 'rb') as f:
            data = f.read()
            assert len(data) == 72
            assert b' \x00\x00\x00' == data[0:4]
            assert b' \x00\x00\x00' == data[36:40]
            private_key = data[4:36]
            public_key = data[40:]
            return cls.faucet_account(private_key)

    @classmethod
    def faucet_file_path(cls):
        curdir = os.path.dirname(libra.__file__)
        return os.path.abspath((os.path.join(curdir, "faucet_key_for_test")))

    def sign(self, message):
        return self._signing_key.sign(message)

    @property
    def address_hex(self):
        return self.address.hex()

    @property
    def public_key(self):
        return self._verify_key.encode()

    @property
    def private_key(self):
        return self._signing_key.encode()

    @property
    def public_key_hex(self):
        return self.public_key.hex()

    @property
    def private_key_hex(self):
        return self.private_key.hex()

