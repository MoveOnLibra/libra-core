from canoser import Struct, ArrayT, MapT
from canoser.struct import TypedProperty
from dataclasses import fields, is_dataclass
import importlib
import typing
#from libra.proto import *


proto_files = [
    'access_path_pb2',
    'account_state_blob_pb2',
    'admission_control_pb2',
    'consensus_pb2',
    'events_pb2',
    'execution_pb2',
    'get_with_proof_pb2',
    'health_checker_pb2',
    'language_storage_pb2',
    'ledger_info_pb2',
    'mempool_pb2',
    'mempool_status_pb2',
    'network_pb2',
    'node_debug_interface_pb2',
    'proof_pb2',
    'secret_service_pb2',
    'state_synchronizer_pb2',
    'storage_pb2',
    'transaction_info_pb2',
    'transaction_pb2',
    'epoch_change_pb2',
    'validator_info_pb2',
    'validator_set_pb2',
    'vm_errors_pb2',
]


def gen_class2protofile():
    ret = {}
    for file in proto_files:
        module_name = f"libra.proto.{file}"
        module = importlib.import_module(module_name)
        clazz = getattr(module, 'DESCRIPTOR')
        for x in clazz.message_types_by_name:
            if x in ret:
                print(f"duplicate message name:{x}")
            else:
                ret[x] = file
    return ret


class2protofile = {'AccessPath': 'access_path_pb2', 'AccountStateBlob': 'account_state_blob_pb2', 'AccountStateWithProof': 'account_state_blob_pb2', 'AdmissionControlMsg': 'admission_control_pb2', 'SubmitTransactionRequest': 'admission_control_pb2', 'AdmissionControlStatus': 'admission_control_pb2', 'SubmitTransactionResponse': 'admission_control_pb2', 'ConsensusMsg': 'consensus_pb2', 'Proposal': 'consensus_pb2', 'SyncInfo': 'consensus_pb2', 'Block': 'consensus_pb2', 'VoteMsg': 'consensus_pb2', 'VoteProposal': 'consensus_pb2', 'RequestBlock': 'consensus_pb2', 'RespondBlock': 'consensus_pb2', 'RequestEpoch': 'consensus_pb2', 'Event': 'events_pb2', 'EventWithProof': 'events_pb2', 'EventsList': 'events_pb2', 'EventsForVersions': 'events_pb2', 'ExecuteBlockRequest': 'execution_pb2', 'ExecuteBlockResponse': 'execution_pb2', 'CommitBlockRequest': 'execution_pb2', 'CommitBlockResponse': 'execution_pb2', 'ExecuteChunkRequest': 'execution_pb2', 'ExecuteChunkResponse': 'execution_pb2', 'UpdateToLatestLedgerRequest': 'get_with_proof_pb2', 'RequestItem': 'get_with_proof_pb2', 'UpdateToLatestLedgerResponse': 'get_with_proof_pb2', 'ResponseItem': 'get_with_proof_pb2', 'GetAccountStateRequest': 'get_with_proof_pb2', 'GetAccountStateResponse': 'get_with_proof_pb2', 'GetAccountTransactionBySequenceNumberRequest': 'get_with_proof_pb2', 'GetAccountTransactionBySequenceNumberResponse': 'get_with_proof_pb2', 'GetEventsByEventAccessPathRequest': 'get_with_proof_pb2', 'GetEventsByEventAccessPathResponse': 'get_with_proof_pb2', 'GetTransactionsRequest': 'get_with_proof_pb2', 'GetTransactionsResponse': 'get_with_proof_pb2', 'HealthCheckerMsg': 'health_checker_pb2', 'Ping': 'health_checker_pb2', 'Pong': 'health_checker_pb2', 'ModuleId': 'language_storage_pb2', 'LedgerInfo': 'ledger_info_pb2', 'LedgerInfoWithSignatures': 'ledger_info_pb2', 'ValidatorSignature': 'ledger_info_pb2', 'AddTransactionWithValidationRequest': 'mempool_pb2', 'AddTransactionWithValidationResponse': 'mempool_pb2', 'GetBlockRequest': 'mempool_pb2', 'GetBlockResponse': 'mempool_pb2', 'TransactionExclusion': 'mempool_pb2', 'CommitTransactionsRequest': 'mempool_pb2', 'CommitTransactionsResponse': 'mempool_pb2', 'CommittedTransaction': 'mempool_pb2', 'HealthCheckRequest': 'mempool_pb2', 'HealthCheckResponse': 'mempool_pb2', 'MempoolAddTransactionStatus': 'mempool_status_pb2', 'PeerInfo': 'network_pb2', 'SignedPeerInfo': 'network_pb2', 'FullNodePayload': 'network_pb2', 'SignedFullNodePayload': 'network_pb2', 'Note': 'network_pb2', 'DiscoveryMsg': 'network_pb2', 'IdentityMsg': 'network_pb2', 'GetNodeDetailsRequest': 'node_debug_interface_pb2', 'GetNodeDetailsResponse': 'node_debug_interface_pb2', 'GetEventsRequest': 'node_debug_interface_pb2', 'GetEventsResponse': 'node_debug_interface_pb2', 'AccumulatorProof': 'proof_pb2', 'SparseMerkleProof': 'proof_pb2', 'AccumulatorConsistencyProof': 'proof_pb2', 'AccumulatorRangeProof': 'proof_pb2', 'SparseMerkleRangeProof': 'proof_pb2', 'TransactionProof': 'proof_pb2', 'AccountStateProof': 'proof_pb2', 'EventProof': 'proof_pb2', 'TransactionListProof': 'proof_pb2', 'GenerateKeyRequest': 'secret_service_pb2', 'GenerateKeyResponse': 'secret_service_pb2', 'PublicKeyRequest': 'secret_service_pb2', 'PublicKeyResponse': 'secret_service_pb2', 'SignRequest': 'secret_service_pb2', 'SignResponse': 'secret_service_pb2', 'GetChunkRequest': 'state_synchronizer_pb2', 'GetChunkResponse': 'state_synchronizer_pb2', 'StateSynchronizerMsg': 'state_synchronizer_pb2', 'SaveTransactionsRequest': 'storage_pb2', 'SaveTransactionsResponse': 'storage_pb2', 'GetLatestStateRootRequest': 'storage_pb2', 'GetLatestStateRootResponse': 'storage_pb2', 'GetLatestAccountStateRequest': 'storage_pb2', 'GetLatestAccountStateResponse': 'storage_pb2', 'GetAccountStateWithProofByVersionRequest': 'storage_pb2', 'GetAccountStateWithProofByVersionResponse': 'storage_pb2', 'GetStartupInfoRequest': 'storage_pb2', 'GetStartupInfoResponse': 'storage_pb2', 'TreeState': 'storage_pb2', 'StartupInfo': 'storage_pb2', 'GetEpochChangeLedgerInfosRequest': 'storage_pb2', 'BackupAccountStateRequest': 'storage_pb2', 'BackupAccountStateResponse': 'storage_pb2', 'GetAccountStateRangeProofRequest': 'storage_pb2', 'GetAccountStateRangeProofResponse': 'storage_pb2', 'TransactionInfo': 'transaction_info_pb2', 'TransactionArgument': 'transaction_pb2', 'SignedTransaction': 'transaction_pb2', 'Transaction': 'transaction_pb2', 'TransactionWithProof': 'transaction_pb2', 'SignedTransactionsBlock': 'transaction_pb2', 'AccountState': 'transaction_pb2', 'TransactionToCommit': 'transaction_pb2', 'TransactionListWithProof': 'transaction_pb2', 'EpochChangeProof': 'epoch_change_pb2', 'ValidatorInfo': 'validator_info_pb2', 'ValidatorSet': 'validator_set_pb2', 'VMStatus': 'vm_errors_pb2'}
#class2protofile = gen_class2protofile()


def get_type_name(ftype):
    if hasattr(ftype, "__name__"):
        return ftype.__name__
    else:
        return ftype.__str__()


class ProtoHelper:
    @staticmethod
    def to_proto(obj):
        if hasattr(obj, "to_proto"):
            return obj.to_proto()
        if isinstance(obj, Struct):
            return ProtoHelper.to_proto_canoser(obj, obj._fields)
        if is_dataclass(obj):
            field_types = [(field.name, field.type) for field in fields(obj)]
            return ProtoHelper.to_proto_dataclass(obj, field_types)
        else:
            return obj

    @staticmethod
    def to_proto_canoser(obj, field_types):
        proto = ProtoHelper.new_proto_obj(obj)
        for fname, ftype in field_types:
            print(fname)
            print(ftype)
            value = getattr(obj, fname)
            if isinstance(value, TypedProperty) or value is None:
                continue
            dest = getattr(proto, fname)
            if isinstance(ftype, ArrayT):
                dest.append(ProtoHelper.to_proto(value))
            elif isinstance(ftype, MapT):
                breakpoint()
            else:
                if hasattr(dest, 'MergeFrom'):
                    dest.MergeFrom(ProtoHelper.to_proto(value))
                else:
                    setattr(proto, fname, ProtoHelper.to_proto(value))
        return proto

    @staticmethod
    def is_list_dataclass(ftype):
        if hasattr(ftype, "__origin__"):
            return ftype.__origin__ == list
        elif isinstance(ftype, str):
            return ftype.startswith("List[")
        else:
            return False

    @staticmethod
    def to_proto_dataclass(obj, field_types):
        proto = ProtoHelper.new_proto_obj(obj)
        for fname, ftype in field_types:
            print(fname)
            print(ftype)
            if hasattr(ftype, "__origin__") and ftype.__origin__ == typing.Union:
                assert ftype.__args__[1] == type(None)
                ftype = ftype.__args__[0]
            value = getattr(obj, fname)
            if value is None:
                continue
            dest = getattr(proto, fname)
            if ProtoHelper.is_list_dataclass(ftype):
                for x in value:
                    dest.append(ProtoHelper.to_proto(x))
            else:
                if hasattr(dest, 'MergeFrom'):
                    dest.MergeFrom(ProtoHelper.to_proto(value))
                else:
                    setattr(proto, fname, ProtoHelper.to_proto(value))
        return proto

    @staticmethod
    def new_proto_obj(obj):
        class_name = obj.__class__.__name__
        if class_name not in class2protofile:
            class_name = obj.__class__.__bases__[0].__name__
        return ProtoHelper.new_proto_by_name(class_name)

    @staticmethod
    def new_proto_by_name(class_name):
        module_name = f"libra.proto.{class2protofile[class_name]}"
        module = importlib.import_module(module_name)
        clazz = getattr(module, class_name)
        instance = clazz()
        return instance
