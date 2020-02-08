from libra.account_state import *
import pytest

def test_state():
	state1 = AccountState.from_blob_or_default(b'\0\0\0\0')
	state2 = AccountState.from_blob_or_default(None)
	assert state1 == state2
	assert state1.get_resource() is None
	with pytest.raises(Exception):
		AccountState.from_blob_or_default(b'')