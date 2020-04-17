from canoser import Struct, Uint64
from libra.language_storage import StructTag, TypeTag
from libra.account_address import ADDRESS_LENGTH, HEX_ADDRESS_LENGTH, Address

CORE_CODE_ADDRESS = b'\x00' * ADDRESS_LENGTH


class AccountConfig:
    # LibraCoin
    COIN_MODULE_NAME = "Libra"
    COIN_STRUCT_NAME = "T"

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
        return "0".rjust(HEX_ADDRESS_LENGTH, '0')

    @classmethod
    def core_code_address_bytes(cls):
        return b'\x00' * ADDRESS_LENGTH

    @classmethod
    def association_address(cls):
        return "a550c18".rjust(HEX_ADDRESS_LENGTH, '0')

    @classmethod
    def association_address_bytes(cls):
        return bytes.fromhex(cls.association_address())

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
            cls.COIN_STRUCT_NAME,
            []
        )

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
        ('receiver', Address),
        ('metadata', bytes)
    ]


class ReceivedPaymentEvent(Struct):
    _fields = [
        ('amount', Uint64),
        ('sender', Address),
        ('metadata', bytes)
    ]
