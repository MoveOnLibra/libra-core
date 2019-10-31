from libra.account_config import *
from libra.event import *
import libra
import pdb

def test_event_sent():
    address = libra.AccountConfig.association_address()
    c = libra.Client("testnet")
    events = c.get_latest_events_sent(address, 2)
    assert len(events) == 2
    assert events[0].transaction_version >= events[1].transaction_version
    contracts = [ContractEvent.from_proto(x.event) for x in events]
    assert contracts[0].key == contracts[1].key
    assert contracts[0].sequence_number-1 == contracts[1].sequence_number
    assert len(contracts[0].event_data) == 40
    aes = [AccountEvent.deserialize(x.event_data) for x in contracts]
    assert aes[0].amount >0
    assert len(aes[0].account) == 32
    assert aes[1].amount >0
    assert len(aes[1].account) == 32
    res = c.get_account_resource(address)
    assert res.sent_events.key == contracts[0].key
    assert res.sent_events.count == contracts[0].sequence_number+1

def test_event_received():
    address = libra.AccountConfig.association_address()
    c = libra.Client("testnet")
    events = c.get_latest_events_received(address, 1)
    if len(events) == 0:
        return
    assert len(events) == 1
    assert events[0].transaction_version > 0
    contracts = [ContractEvent.from_proto(x.event) for x in events]
    assert len(contracts[0].event_data) == 40
    aes = [AccountEvent.deserialize(x.event_data) for x in contracts]
    assert aes[0].amount >0
    assert len(aes[0].account) == 32
    res = c.get_account_resource(address)
    assert res.received_events.key == contracts[0].key
    assert res.received_events.count == contracts[0].sequence_number+1
