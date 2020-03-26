from libra.access_path import *
from libra.account_config import AccountConfig
from libra.language_storage import ModuleId

#import pdb

def test_resource_access_vec():
    array = AccessPath.resource_access_vec(AccountConfig.account_struct_tag(), [])
    assert bytes(array) == AccountConfig.account_resource_path()

def test_code_access_path():
    address = b'1' * Address.LENGTH
    mid = ModuleId(address, 'Pay')
    assert mid.address == address
    assert mid.name == 'Pay'
    path = AccessPath.code_access_path_vec(mid)
    assert len(path) == 33
    assert path[0] == 0
    assert bytes(path).hex() == "004f37ea258b9fbef8e67caccde1ff4a9b8d54e48a19efcb4eae6ab0230393257b"
    ap = AccessPath.code_access_path(mid)
    assert ap.address == address
    assert ap.path == path