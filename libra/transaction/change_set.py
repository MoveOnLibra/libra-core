from canoser import Struct
from libra.transaction.write_set import WriteSet
from libra.contract_event import ContractEvent


class ChangeSet(Struct):

    _fields = [
        ('write_set', WriteSet),
        ('events', [ContractEvent])
    ]

    def to_json_serializable(self):
        amap = super().to_json_serializable()
        if hasattr(self, 'transaction_info'):
            amap["transaction_info"] = self.transaction_info.to_json_serializable()
        if hasattr(self, 'version'):
            amap["version"] = self.version
        if hasattr(self, 'success'):
            amap["success"] = self.success
        return amap
