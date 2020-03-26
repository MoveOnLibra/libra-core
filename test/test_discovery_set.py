from libra.discovery_set import DiscoverySet
from libra.event import EVENT_KEY_LENGTH

def test_discovery_set():
    key = DiscoverySet.change_event_key()
    assert len(key) == EVENT_KEY_LENGTH
    assert key.hex() == '0200000000000000000000000000000000000000000d15c0'