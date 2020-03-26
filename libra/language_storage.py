from canoser import Struct, RustEnum, Uint64, Uint8, Uint128
from libra.account_address import Address
from libra.identifier import Identifier
from libra.hasher import gen_hasher
import libra

class StructTag(Struct):
    _fields = [
        ('address', Address),
        ('module', Identifier),
        ('name', Identifier),
        ('type_params', ['libra.language_storage.TypeTag'])
    ]

    def hash(self):
        shazer = gen_hasher(b"StructTag::libra_types::language_storage")
        shazer.update(self.serialize())
        return shazer.digest()

    def is_pay_tag(self):
        return self.address == libra.AccountConfig.core_code_address_bytes() and\
                self.module == libra.AccountConfig.ACCOUNT_MODULE_NAME and\
                (self.name == "SentPaymentEvent" or self.name == "ReceivedPaymentEvent")


class TypeTag(RustEnum):
    _enums = [
        ('Bool', None),
        ('U8', None),
        ('U64', None),
        ('U128', None),
        ('Address', None),
        ('Vector', 'libra.language_storage.TypeTag'),
        ('Struct', StructTag)
    ]



class ResourceKey(Struct):
    """Represents the intitial key into global storage where we first index by the address, and then the struct tag"""
    _fields = [
        ('address', Address),
        ('type_', StructTag)
    ]


class ModuleId(Struct):
    _fields = [
        ('address', Address),
        ('name', Identifier)
    ]

    def hash(self):
        shazer = gen_hasher(b"ModuleId::libra_types::language_storage")
        shazer.update(self.serialize())
        return shazer.digest()

    def __hash__(self):
        return (self.address, self.name).__hash__()

    def into(self):
        from libra.access_path import AccessPath
        return AccessPath.code_access_path(self)