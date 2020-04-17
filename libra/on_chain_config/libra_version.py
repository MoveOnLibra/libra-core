from __future__ import annotations
from libra.on_chain_config.on_chain_config import OnChainConfig
from canoser import Struct, Uint64

# Defines the version of Libra Validator software.


class LibraVersion(Struct, OnChainConfig):
    _fields = [
        ('major', Uint64),
    ]

    IDENTIFIER: str = "LibraVersion"
