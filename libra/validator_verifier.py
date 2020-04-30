from canoser import Struct, Uint64, BytesT
from libra.crypto.ed25519 import ED25519_PUBLIC_KEY_LENGTH
from libra.account_address import Address
from nacl.signing import VerifyKey


class VerifyError(Exception):
    pass


class ValidatorConsensusInfo(Struct):
    _fields = [
        ('public_key', BytesT(ED25519_PUBLIC_KEY_LENGTH)),
        ('voting_power', Uint64)
    ]


class ValidatorVerifier(Struct):
    _fields = [
        ('address_to_validator_info', {Address: ValidatorConsensusInfo}),
        ('quorum_voting_power', Uint64),
        ('total_voting_power', Uint64)
    ]

    @classmethod
    def new(cls, address_to_validator_info):
        ret = cls()
        ret.address_to_validator_info = address_to_validator_info
        ret.total_voting_power = sum([v.voting_power for k, v in address_to_validator_info.items()])
        if len(address_to_validator_info) == 0:
            ret.quorum_voting_power = 0
        else:
            ret.quorum_voting_power = ret.total_voting_power * 2 // 3 + 1
        return ret

    def batch_verify_aggregated_signature(self, ledger_info_hash, signatures):
        self.check_num_of_signatures(signatures)
        self.check_keys(signatures)
        self.check_voting_power(signatures)
        # TODO: PublicKey::batch_verify_signatures(&hash, keys_and_signatures)
        self.verify_aggregated_signature(ledger_info_hash, signatures)

    def check_num_of_signatures(self, signatures):
        num = len(signatures)
        if num > len(self.address_to_validator_info):
            raise VerifyError(f"TooManySignatures: {num} > {len(self.address_to_validator_info)}")

    def check_voting_power(self, signatures):
        aggregated_voting_power = 0
        for addr, _sign in signatures.items():
            aggregated_voting_power += self.get_voting_power(addr)
        if aggregated_voting_power < self.quorum_voting_power:
            raise VerifyError(f"TooLittleVotingPower: {aggregated_voting_power} > {self.quorum_voting_power}")

    def get_voting_power(self, address):
        return self.address_to_validator_info[address].voting_power

    def check_keys(self, signatures):
        for addr, _sign in signatures.items():
            if addr not in self.address_to_validator_info:
                raise VerifyError(f"UnknownAuthor: {addr}")

    def verify_aggregated_signature(self, ledger_info_hash, signatures):
        for addr, signature in signatures.items():
            self.verify_signature(addr, ledger_info_hash, signature)

    def verify_signature(self, address, ledger_info_hash, signature):
        validator_info = self.address_to_validator_info[address]
        vkey = VerifyKey(bytes(validator_info.public_key))
        vkey.verify(ledger_info_hash, bytes(signature))
