from canoser import BytesT, DelegateT
from nacl.signing import SigningKey
from nacl.public import PrivateKey
from typing import Tuple

ED25519_PRIVATE_KEY_LENGTH = 32
ED25519_PUBLIC_KEY_LENGTH = 32
ED25519_SIGNATURE_LENGTH = 64

class Ed25519PrivateKey(DelegateT):
    delegate_type = BytesT(ED25519_PRIVATE_KEY_LENGTH)

class Ed25519PublicKey(DelegateT):
    delegate_type = BytesT(ED25519_PUBLIC_KEY_LENGTH)

class Ed25519Signature(DelegateT):
    delegate_type = BytesT(ED25519_SIGNATURE_LENGTH)


# Generate an arbitrary key pair, with possible Rng input
    #
# Warning: if you pass in None, this will not return distinct
# results every time! Should you want to write non-deterministic
# tests, look at libra_config.config_builder.util.get_test_config
def generate_keypair(seed) -> Tuple[Ed25519PrivateKey, Ed25519PublicKey]:
	#TODO: FIXME
	if seed is None:
		private_key = bytes.fromhex("82001573a003fd3b7fd72ffb0eaf63aac62f12deb629dca72785a66268ec758b")
		#This private_key is generated by libra/rust.
		return _generate_keypair_by_private_key(private_key)
	else:
		skbob = PrivateKey.generate()
		return _generate_keypair_by_private_key(skbob.encode())



# Generates a well-known keypair `(Ed25519PrivateKey, Ed25519PublicKey)` for special use
# in the genesis block. A genesis block is the first block of a blockchain and it is
# hardcoded as it's a special case in that it does not reference a previous block.
def generate_genesis_keypair() -> Tuple[Ed25519PrivateKey, Ed25519PublicKey]:
	buf = [0] * ED25519_PRIVATE_KEY_LENGTH
	buf[ED25519_PRIVATE_KEY_LENGTH - 1] = 1
	private_key = bytes(buf)
	return _generate_keypair_by_private_key(private_key)

def _generate_keypair_by_private_key(private_key) -> Tuple[Ed25519PrivateKey, Ed25519PublicKey]:
	_signing_key = SigningKey(private_key)
	_verify_key = _signing_key.verify_key
	public_key = _verify_key.encode()
	return (private_key, public_key)