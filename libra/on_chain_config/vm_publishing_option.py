from __future__ import annotations
from libra.on_chain_config.on_chain_config import OnChainConfig
from libra.hasher import HashValue
from libra.transaction import SCRIPT_HASH_LENGTH
from canoser import RustEnum, BytesT, Cursor

# Defines and holds the publishing policies for the VM. There are three possible configurations:
# 1. No module publishing, only whitelisted scripts are allowed.
# 2. No module publishing, custom scripts are allowed.
# 3. Both module publishing and custom scripts are allowed.
# We represent these as an enum instead of a struct since whitelisting and module/script
# publishing are mutually exclusive options.


class VMPublishingOption(RustEnum, OnChainConfig):
    _enums = [
        # Only allow scripts on a whitelist to be run
        ('Locked', [BytesT(SCRIPT_HASH_LENGTH)]),
        # Allow custom scripts, but _not_ custom module publishing
        ('CustomScripts', None),
        # Allow both custom scripts and custom module publishing
        ('Open', None)
    ]

    IDENTIFIER: str = "ScriptWhitelist"

    def deserialize_into_config(cls, v: bytes) -> VMPublishingOption:
        deser = BytesT.decode(Cursor(v))
        return cls.deserialize_default_impl(deser)

    def is_open(self) -> bool:
        return self.Open

    def is_allowed_script(self, program: bytes) -> bool:
        if self.Open or self.CustomScripts:
            return True
        hash_value = HashValue.from_sha3_256(program)
        return hash_value in self.value
