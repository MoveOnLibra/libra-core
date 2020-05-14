from libra.access_path import *
from libra.account_config import AccountConfig
from libra.account_resource import AccountResource
from libra.language_storage import ModuleId

#import pdb

def test_resource_access_vec():
    array = AccessPath.resource_access_vec(AccountResource.struct_tag(), [])
    assert bytes(array) == AccountResource.resource_path()

def test_code_access_path():
    address = b'1' * Address.LENGTH
    mid = ModuleId(address, 'Pay')
    assert mid.address == address
    assert mid.name == 'Pay'
    path = AccessPath.code_access_path_vec(mid)
    assert len(path) == 33
    assert path[0] == 0
    assert bytes(path).hex() == "00a13546297a05f032a52d9339c577c664119572497130b366b4719b6a7a3c844f"
    ap = AccessPath.code_access_path(mid)
    assert ap.address == address
    assert ap.path == path
    print(ap)