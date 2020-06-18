from __future__ import annotations
from libra.move_resource import MoveResource
from libra.crypto.ed25519 import Ed25519PublicKey
from libra.crypto.x25519 import X25519PublicKey
from canoser import Struct, BytesT

Multiaddr = BytesT()


class ValidatorConfig(Struct):
    _fields = [
        ('consensus_public_key', Ed25519PublicKey),
        ('validator_network_signing_pubkey', Ed25519PublicKey),
        ('validator_network_identity_pubkey', X25519PublicKey),
        ('validator_network_address', Multiaddr),
        ('fullnodes_network_identity_pubkey', X25519PublicKey),
        ('fullnodes_network_address', Multiaddr)
    ]


class ValidatorConfigResource(Struct, MoveResource):
    _fields = [
        ('validator_config', ValidatorConfig),
    ]

    MODULE_NAME: str = "ValidatorConfig"
    STRUCT_NAME: str = MODULE_NAME
