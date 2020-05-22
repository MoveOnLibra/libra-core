from canoser import Struct, Uint64, Uint128
from libra.event import EventHandle
from libra.access_path import AccessPath, Accesses
from libra.account_config import AccountConfig
from libra.move_resource import MoveResource
from libra.language_storage import TypeTag, StructTag
from libra.rustlib import bail
from typing import List

Identifier = str

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
        ('is_frozen', bool),
    ]


    MODULE_NAME: str = AccountConfig.ACCOUNT_MODULE_NAME
    STRUCT_NAME: str = "T"

    @classmethod
    def get_account_resource_or_default(cls, blob):
        # TODO: remove this method
        from libra.account_state import AccountState
        if blob:
            omap = AccountState.deserialize(blob.blob).ordered_map
            path = AccountResource.resource_path()
            if path in omap:
                resource = omap[path]
                return cls.deserialize(resource)

        return cls()

    def get_event_handle_by_query_path(self, query_path):
        if AccountConfig.account_received_event_path() == query_path:
            return self.received_events
        elif AccountConfig.account_sent_event_path() == query_path:
            return self.sent_events
        else:
            bail("Unrecognized query path: {}", query_path)


# The balance resource held under an account.
class BalanceResource(Struct, MoveResource):
    _fields = [
        ('coin', Uint64)
    ]

    @classmethod
    def type_params(cls) -> List[TypeTag]:
        return [AccountConfig.lbr_type_tag()]

    # TODO/XXX: remove this once the MoveResource trait allows type arguments to `struct_tag`.
    @classmethod
    def struct_tag_for_currency(cls, currency_typetag: TypeTag) -> StructTag:
        return StructTag(
            address= AccountConfig.core_code_address_bytes(),
            name= BalanceResource.struct_identifier(),
            module= BalanceResource.module_identifier(),
            type_params= [currency_typetag],
        )


    # TODO: remove this once the MoveResource trait allows type arguments to `resource_path`.
    @classmethod
    def access_path_for(cls, currency_typetag: TypeTag) -> bytes:
        return AccessPath.resource_access_vec(
            BalanceResource.struct_tag_for_currency(currency_typetag),
            Accesses.empty(),
        )

    MODULE_NAME: str = AccountConfig.ACCOUNT_MODULE_NAME
    STRUCT_NAME: str = "Balance"


class AssociationCapabilityResource(Struct):
    _fields = [
        ('is_certified', bool)
    ]


class CurrencyInfoResource(Struct, MoveResource):
    _fields = [
        ('total_value', Uint128),
        ('preburn_value', Uint64),
        ('to_lbr_exchange_rate', Uint64),
        ('is_synthetic', bool),
        ('scaling_factor', Uint64),
        ('fractional_part', Uint64),
        ('currency_code', Identifier),
        ('can_mint', bool),
    ]

    MODULE_NAME: str = "Libra"
    STRUCT_NAME: str = "CurrencyInfo"

