from libra.vm_error import *
from libra.transaction import *
import libra
from canoser import Uint64
import pytest

def test_status_code():
    assert StatusCode.INVALID_SIGNATURE == 1
    assert isinstance(StatusCode.INVALID_SIGNATURE, int)
    assert StatusCode.UNKNOWN_STATUS == Uint64.max_value
    assert StatusCode.get_name(1) == "INVALID_SIGNATURE"

def test_vm_error():
    status = VMStatus(4016).with_message("test msg")
    assert status.status_type() == StatusType.Execution
    assert status.message == "test msg"
    ts = TransactionStatus.from_vm_status(status)
    assert ts.tag == TransactionStatus.Keep
    assert ts.vm_status == status


def test_vm_error2():
    status = VMStatus(Uint64.max_value)
    assert status.status_type() == StatusType.Unknown
    ts = TransactionStatus.from_vm_status(status)
    assert ts.tag == TransactionStatus.Discard
    assert ts.vm_status == status