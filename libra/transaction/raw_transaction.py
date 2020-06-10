from canoser import Struct, Uint64
from datetime import datetime
from libra.account_address import Address
from libra.hasher import LCSCryptoHash
from libra.transaction.transaction_payload import TransactionPayload
from libra.transaction.script import Script
from nacl.signing import SigningKey
from libra.transaction.authenticator import TransactionAuthenticator

MAX_GAS_AMOUNT = 1_000_000


class RawTransaction(Struct, LCSCryptoHash):
    """RawTransaction is the portion of a transaction that a client signs.
    It can be either to publish a module, to execute a script, or to issue a writeset transaction.
    """
    _fields = [
        ('sender', Address),
        ('sequence_number', Uint64),
        ('payload', TransactionPayload),
        ('max_gas_amount', Uint64),
        ('gas_unit_price', Uint64),
        ('gas_currency_code', str),
        ('expiration_time', Uint64),
    ]

    @classmethod
    def new_change_set(cls, sender_address, sequence_number, change_set):
        return RawTransaction(
            sender_address, sequence_number,
            TransactionPayload('WriteSet', change_set),
            # Since write-set transactions bypass the VM, these fields aren't relevant.
            0, 0, "LBR",
            # Write-set transactions are special and important and shouldn't expire.
            Uint64.max_value
        )

    @classmethod
    def new_script_tx(cls, sender_address, sequence_number, script, **kwargs):
        """Create a new `RawTransaction` with a script.
        A script transaction contains only code to execute. No publishing is allowed in scripts.
        """
        payload = TransactionPayload('Script', script)
        return cls.new_tx(sender_address, sequence_number, payload, **kwargs)

    @classmethod
    def new_tx(cls, sender_address, sequence_number, payload, **kwargs):
        sender_address = Address.normalize_to_bytes(sender_address)
        default_args = {
            "max_gas_amount":MAX_GAS_AMOUNT,
            "gas_unit_price":0,
            "gas_currency_code":"LBR",
            "txn_expiration":100,
        }
        default_args.update(kwargs)
        return RawTransaction(
            sender_address,
            sequence_number,
            payload,
            default_args['max_gas_amount'],
            default_args['gas_unit_price'],
            default_args['gas_currency_code'],
            int(datetime.now().timestamp()) + default_args['txn_expiration']
        )

    @classmethod
    def _gen_transfer_transaction(cls, sender_address, sequence_number, receiver_address,
                                  micro_libra, **kwargs):
        script = Script.gen_transfer_script(receiver_address, micro_libra, **kwargs)
        return RawTransaction.new_script_tx(
            sender_address,
            sequence_number,
            script,
            **kwargs
        )

    def sign(self, private_key, public_key):
        from libra.transaction.signed_transaction import SignedTransaction, SignatureCheckedTransaction
        _signing_key = SigningKey(private_key)
        signature = _signing_key.sign(self.hash())[:64]
        assert len(signature) == 64
        authenticator = TransactionAuthenticator.ed25519(public_key, signature)
        return SignatureCheckedTransaction(
            SignedTransaction(self, authenticator)
        )
