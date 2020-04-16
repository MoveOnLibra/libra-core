from canoser import Struct, Uint8, Uint64
from libra.event import EventHandle
from libra.account_config import AccountConfig
from libra.move_resource import MoveResource
from libra.language_storage import TypeTag
from libra.rustlib import bail
from io import StringIO
from typing import List


class AccountResource(Struct, MoveResource):
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

    MODULE_NAME: str = AccountConfig.ACCOUNT_MODULE_NAME
    STRUCT_NAME: str = "T"


    @classmethod
    def get_account_resource_or_default(cls, blob):
        #TODO: remove this method
        from libra.account_state import AccountState
        if blob:
            try:
                omap = AccountState.deserialize(blob.blob).ordered_map
                resource = omap[AccountResource.resource_path()]
                return cls.deserialize(resource)
            except Exception:
                return cls()
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
class BalanceResource(Struct, MoveResource):
    _fields = [
        ('coin', Uint64)
    ]

    @classmethod
    def type_params(cls) -> List[TypeTag]:
        return [AccountConfig.lbr_type_tag()]


    MODULE_NAME: str = AccountConfig.ACCOUNT_MODULE_NAME
    STRUCT_NAME: str = "Balance"
