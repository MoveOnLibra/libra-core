from libra.account_state import *
from libra.account_resource import AccountResource, BalanceResource
import pytest

def test_state():
	state1 = AccountState.from_blob_or_default(b'\0')
	state2 = AccountState.from_blob_or_default(None)
	assert state1 == state2
	assert state1.get_move_resource(AccountResource) is None
	with pytest.raises(Exception):
		AccountState.from_blob_or_default(b'')

def test_parse_resource():
    state1 = AccountState.from_blob_or_default(b'\0')
    state1.get_account_resource()
    state1.get_balance_resource("LBR")
    state1.get_configuration_resource()
    state1.get_discovery_set_resource()
    state1.get_libra_timestamp_resource()
    state1.get_validator_config_resource()
    state1.get_validator_set()
    state1.get_libra_block_resource()

