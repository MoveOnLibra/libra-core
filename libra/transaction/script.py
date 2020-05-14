from canoser import Struct
from libra.transaction.transaction_argument import TransactionArgument, normalize_public_key
from libra.transaction_scripts import bytecodes
from libra.account_address import Address
from libra.account_config import AccountConfig
from libra.language_storage import TypeTag


class Script(Struct):
    _fields = [
        ('code', bytes),
        ('ty_args', [TypeTag]),
        ('args', [TransactionArgument])
    ]

    @classmethod
    def gen_transfer_script(cls,
                            receiver_address,
                            micro_libra,
                            metadata=None,
                            auth_key_prefix=None,
                            ):
        if isinstance(receiver_address, list):
            receiver_address = bytes(receiver_address)
        if isinstance(receiver_address, str):
            receiver_address = bytes.fromhex(receiver_address)
        if auth_key_prefix is None:
            auth_key_prefix = b''
        if metadata is None:
            code = bytecodes["peer_to_peer"]
            args = [
                TransactionArgument('Address', receiver_address),
                TransactionArgument('U8Vector', auth_key_prefix),
                TransactionArgument('U64', micro_libra)
            ]
        else:
            code = bytecodes["peer_to_peer_with_metadata"]
            metadata_signature = b''
            # TODO: how to generate metadata_signature?
            args = [
                TransactionArgument('Address', receiver_address),
                TransactionArgument('U8Vector', auth_key_prefix),
                TransactionArgument('U64', micro_libra),
                TransactionArgument('U8Vector', metadata),
                TransactionArgument('U8Vector', metadata_signature)
            ]
        ty_args = [AccountConfig.lbr_type_tag()]
        return Script(code, ty_args, args)

    @classmethod
    def gen_mint_script(cls, receiver_address, auth_key_prefix, micro_libra):
        receiver_address = Address.normalize_to_bytes(receiver_address)
        code = bytecodes["mint"]
        args = [
            TransactionArgument('Address', receiver_address),
            TransactionArgument('U8Vector', auth_key_prefix),
            TransactionArgument('U64', micro_libra)
        ]
        return Script(code, [AccountConfig.lbr_type_tag()], args)

    @classmethod
    def gen_create_account_script(cls, fresh_address, auth_key_prefix, initial_balance=0):
        fresh_address = Address.normalize_to_bytes(fresh_address)
        code = bytecodes["create_account"]
        args = [
            TransactionArgument('Address', fresh_address),
            TransactionArgument('U8Vector', auth_key_prefix),
            TransactionArgument('U64', initial_balance)
        ]
        return Script(code, [AccountConfig.lbr_type_tag()], args)

    @classmethod
    def gen_rotate_auth_key_script(cls, public_key):
        key = normalize_public_key(public_key)
        code = bytecodes["rotate_authentication_key"]
        args = [
            TransactionArgument('U8Vector', key)
        ]
        return Script(code, [], args)

    @classmethod
    def gen_rotate_consensus_pubkey_script(cls, public_key):
        key = normalize_public_key(public_key)
        code = bytecodes["rotate_consensus_pubkey"]
        args = [
            TransactionArgument('U8Vector', key)
        ]
        return Script(code, [], args)

    @classmethod
    def gen_add_validator_script(cls, address):
        address = Address.normalize_to_bytes(address)
        code = bytecodes["add_validator"]
        args = [
            TransactionArgument('Address', address)
        ]
        return Script(code, [], args)

    @classmethod
    def gen_remove_validator_script(cls, address):
        address = Address.normalize_to_bytes(address)
        code = bytecodes["remove_validator"]
        args = [
            TransactionArgument('Address', address)
        ]
        return Script(code, [], args)

    @classmethod
    def gen_register_validator_script(cls,
                                      consensus_pubkey,
                                      validator_network_signing_pubkey,
                                      validator_network_identity_pubkey,
                                      validator_network_address,
                                      fullnodes_network_identity_pubkey,
                                      fullnodes_network_address
                                      ):
        validator_network_address = Address.normalize_to_bytes(validator_network_address)
        fullnodes_network_address = Address.normalize_to_bytes(fullnodes_network_address)
        consensus_pubkey = normalize_public_key(consensus_pubkey)
        validator_network_signing_pubkey = normalize_public_key(validator_network_signing_pubkey)
        validator_network_identity_pubkey = normalize_public_key(validator_network_identity_pubkey)
        fullnodes_network_identity_pubkey = normalize_public_key(fullnodes_network_identity_pubkey)
        code = bytecodes["register_validator"]
        args = [
            TransactionArgument('U8Vector', consensus_pubkey),
            TransactionArgument('U8Vector', validator_network_signing_pubkey),
            TransactionArgument('U8Vector', validator_network_identity_pubkey),
            TransactionArgument('Address', validator_network_address),
            TransactionArgument('U8Vector', fullnodes_network_identity_pubkey),
            TransactionArgument('Address', fullnodes_network_address)
        ]
        return Script(code, [], args)

    @staticmethod
    def get_script_bytecode(script_name):
        return bytecodes[script_name]
