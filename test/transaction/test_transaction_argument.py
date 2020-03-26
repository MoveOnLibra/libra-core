from libra.transaction import *
from libra.account_config import AccountConfig
import pytest
#import pdb

def test_parse_as_transaction_argument():
    address = bytes.fromhex("0000000000000000000000000a550c18")
    addr = TransactionArgument.parse_as_transaction_argument(AccountConfig.association_address())
    assert bytes(addr.value) == address
    assert addr.Address
    hello = TransactionArgument.parse_as_transaction_argument('b"48656c6c6f20776f726c6421"')
    assert hello.U8Vector
    assert bytes(hello.value) == b"Hello world!"
    i = TransactionArgument.parse_as_transaction_argument('1234')
    assert i.U64
    assert i.value == 1234
    b = TransactionArgument.parse_as_transaction_argument('true')
    assert b.Bool
    assert b.value == True
    with pytest.raises(Exception):
        TransactionArgument.parse_as_transaction_argument('abc')
    with pytest.raises(Exception):
        TransactionArgument.parse_as_transaction_argument('-1')
    with pytest.raises(Exception):
        TransactionArgument.parse_as_transaction_argument(AccountConfig.association_address()+"0")