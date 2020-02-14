from libra.crypto.ed25519 import *

def test_generate_genesis_keypair():
	privk, pubk = generate_genesis_keypair()
	assert len(privk) == 32
	assert len(pubk) == 32
	assert pubk.hex() == "4cb5abf6ad79fbf5abbccafcc269d85cd2651ed4b885b5869f241aedf0a5ba29"


def test_generate_keypair():
	privk, pubk = generate_keypair(None)
	assert len(privk) == 32
	assert len(pubk) == 32
	assert pubk.hex() == "664f6e8f36eacb1770fa879d86c2c1d0fafea145e84fa7d671ab7a011a54d509"
