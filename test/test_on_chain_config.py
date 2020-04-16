from libra.on_chain_config import *

def test_on_chain_config():
    ver = LibraVersion(2)
    ver2 = LibraVersion.deserialize_into_config(ver.serialize())
    assert ver == ver2
