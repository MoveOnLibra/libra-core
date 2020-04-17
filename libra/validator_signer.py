from __future__ import annotations
from libra.account_address import Address
from libra.crypto.ed25519 import Ed25519PrivateKey, Ed25519PublicKey, Ed25519Signature
from libra.hasher import HashValue
from nacl.signing import SigningKey
from dataclasses import dataclass

# ValidatorSigner associates an author with public and private keys with helpers for signing and
# validating. This struct can be used for all signing operations including block and network
# signing, respectively.
@dataclass
class ValidatorSigner:
    author: Address
    private_key: Ed25519PrivateKey

    # Constructs a signature for `message` using `private_key`.

    def sign_message(self, message: HashValue) -> Ed25519Signature:
        _signing_key = SigningKey(self.private_key)
        return _signing_key.sign(message)

    # Returns the public key associated with this signer.

    def public_key(self) -> Ed25519PublicKey:
        _signing_key = SigningKey(self.private_key)
        _verify_key = _signing_key.verify_key
        return _verify_key.encode()
