from canoser import Struct, Uint64
from libra.language_storage import StructTag, TypeTag
from libra.account_address import ADDRESS_LENGTH, HEX_ADDRESS_LENGTH, Address

Identifier = str

CORE_CODE_ADDRESS = b'\x00' * ADDRESS_LENGTH


class AccountConfig:
    # LibraCoin
    COIN_MODULE_NAME = "Libra"
    COIN_STRUCT_NAME = "Libra"

    LBR_NAME = "LBR"

    # Account
    ACCOUNT_MODULE_NAME = "LibraAccount"

    ACCOUNT_EVENT_HANDLE_STRUCT_NAME = "EventHandle"
    ACCOUNT_EVENT_HANDLE_GENERATOR_STRUCT_NAME = "EventHandleGenerator"

    # Hash
    HASH_MODULE_NAME = "Hash"

    @classmethod
    def account_sent_event_path(cls):
        from libra.account_resource import AccountResource
        return AccountResource.resource_path() + b"/sent_events_count/"

    @classmethod
    def account_received_event_path(cls):
        from libra.account_resource import AccountResource
        return AccountResource.resource_path() + b"/received_events_count/"

    @classmethod
    def core_code_address(cls):
        return "1".rjust(HEX_ADDRESS_LENGTH, '0')

    @classmethod
    def core_code_address_bytes(cls):
        return bytes.fromhex(cls.core_code_address())

    @classmethod
    def association_address(cls):
        return "a550c18".rjust(HEX_ADDRESS_LENGTH, '0')

    @classmethod
    def association_address_bytes(cls):
        return bytes.fromhex(cls.association_address())

    @classmethod
    def treasury_compliance_account_address(cls):
        return "b1e55ed".rjust(HEX_ADDRESS_LENGTH, '0')

    @classmethod
    def treasury_compliance_account_address_bytes(cls):
        return bytes.fromhex(cls.treasury_compliance_account_address())

    @classmethod
    def transaction_fee_address(cls):
        return "FEE".rjust(HEX_ADDRESS_LENGTH, '0')

    @classmethod
    def transaction_fee_address_bytes(cls):
        return bytes.fromhex(cls.transaction_fee_address())

    @classmethod
    def validator_set_address(cls):
        return "1d8".rjust(HEX_ADDRESS_LENGTH, '0')

    @classmethod
    def validator_set_address_bytes(cls):
        return bytes.fromhex(cls.validator_set_address())

    @classmethod
    def discovery_set_address(cls):
        return "D15C0".rjust(HEX_ADDRESS_LENGTH, '0')

    @classmethod
    def discovery_set_address_bytes(cls):
        return bytes.fromhex(cls.discovery_set_address())

    @classmethod
    def lbr_type_tag(cls) -> TypeTag:
        return TypeTag('Struct', cls.lbr_struct_tag())

    @classmethod
    def lbr_struct_tag(cls):
        return StructTag(
            cls.core_code_address_bytes(),
            cls.LBR_NAME,
            cls.LBR_NAME,
            []
        )

    @classmethod
    def account_type_struct_tag(cls, is_empty_account_type: bool) -> StructTag:
        if is_empty_account_type:
            inner_struct_tag = StructTag(
                address= CORE_CODE_ADDRESS,
                module= "Empty",
                name= "Empty",
                type_params= [],
            )
        else:
            inner_struct_tag = StructTag(
                address= CORE_CODE_ADDRESS,
                module= "Unhosted",
                name= "Unhosted",
                type_params= [],
            )

        return StructTag(
            address= CORE_CODE_ADDRESS,
            module= "AccountType",
            name= "AccountType",
            type_params= [TypeTag('Struct', inner_struct_tag)],
        )


    # TODO: This imposes a few implied restrictions:
    #   1) The currency module must be published under the core code address.
    #   2) The module name must be the same as the gas specifier.
    #   3) The struct name must be the same as the module name.
    # We need to consider whether we want to switch to a more or fully qualified name.
    @classmethod
    def account_balance_struct_tag(cls) -> StructTag:
        return StructTag(
            address= CORE_CODE_ADDRESS,
            module= "LibraAccount",
            name= "Balance",
            type_params= [cls.lbr_type_tag()],
        )

    @classmethod
    def event_handle_generator_struct_tag(cls) -> StructTag:
        return StructTag(
            address= CORE_CODE_ADDRESS,
            module= "Event",
            name= "EventHandleGenerator",
            type_params= [],
        )

    @classmethod
    def type_tag_for_currency_code(cls, currency_code: Identifier) -> TypeTag:
        return TypeTag('Struct', StructTag(
            address= CORE_CODE_ADDRESS,
            module= currency_code,
            name= cls.COIN_STRUCT_NAME,
            type_params= [],
        ))


    @classmethod
    def all_config(cls):
        from libra.account_resource import AccountResource
        return {
            "core_code_address": AccountConfig.core_code_address(),
            "association_address": AccountConfig.association_address(),
            "transaction_fee_address": AccountConfig.transaction_fee_address(),
            "validator_set_address": AccountConfig.validator_set_address(),
            "account_resource_path": AccountResource.resource_path(),
            "account_sent_event_path": AccountConfig.account_sent_event_path(),
            "account_received_event_path": AccountConfig.account_received_event_path()
        }


class SentPaymentEvent(Struct):
    _fields = [
        ('amount', Uint64),
        ('currency_code', Identifier),
        ('receiver', Address),
        ('metadata', bytes)
    ]


class ReceivedPaymentEvent(Struct):
    _fields = [
        ('amount', Uint64),
        ('currency_code', Identifier),
        ('sender', Address),
        ('metadata', bytes)
    ]
