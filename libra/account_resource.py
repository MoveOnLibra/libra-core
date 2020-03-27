from canoser import Struct, Uint8, Uint64
from libra.event import EventHandle
from libra.account_config import AccountConfig
from libra.rustlib import bail
from io import StringIO


class AccountResource(Struct):
    """
    A Rust/Python representation of an Account resource.
    This is not how the Account is represented in the VM but it's a convenient representation.
    """
    _fields = [
        ('authentication_key', bytes),
        ('delegated_key_rotation_capability', bool),
        ('delegated_withdrawal_capability', bool),
        ('received_events', EventHandle),
        ('sent_events', EventHandle),
        ('sequence_number', Uint64),
        ('event_generator', Uint64)
    ]

    @classmethod
    def get_account_resource_or_default(cls, blob):
        #TODO: remove this method
        from libra.account_state import AccountState
        if blob:
            omap = AccountState.deserialize(blob.blob).ordered_map
            resource = omap[AccountConfig.account_resource_path()]
            return cls.deserialize(resource)
        else:
            return cls()

    def get_event_handle_by_query_path(self, query_path):
        if AccountConfig.account_received_event_path() == query_path:
            return self.received_events
        elif AccountConfig.account_sent_event_path() == query_path:
            return self.sent_events
        else:
            bail("Unrecognized query path: {}", query_path);



# The balance resource held under an account.
class BalanceResource(Struct):
    _fields = [
        ('coin', Uint64)
    ]

