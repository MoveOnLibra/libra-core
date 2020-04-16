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
    assert bytes(path).hex() == "0084eb49a874bc95da42abebc3ca4938db7535a1cc364d576792879bb6053cde01"
    ap = AccessPath.code_access_path(mid)
    assert ap.address == address
    assert ap.path == path
    print(ap)