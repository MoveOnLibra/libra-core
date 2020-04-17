# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import get_with_proof_pb2 as get__with__proof__pb2
import storage_pb2 as storage__pb2
import validator_change_pb2 as validator__change__pb2


class StorageStub(object):
    """-----------------------------------------------------------------------------
    ---------------- Service definition for storage
    -----------------------------------------------------------------------------
    Write APIs.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SaveTransactions = channel.unary_unary(
            '/storage.Storage/SaveTransactions',
            request_serializer=storage__pb2.SaveTransactionsRequest.SerializeToString,
            response_deserializer=storage__pb2.SaveTransactionsResponse.FromString,
        )
        self.UpdateToLatestLedger = channel.unary_unary(
            '/storage.Storage/UpdateToLatestLedger',
            request_serializer=get__with__proof__pb2.UpdateToLatestLedgerRequest.SerializeToString,
            response_deserializer=get__with__proof__pb2.UpdateToLatestLedgerResponse.FromString,
        )
        self.GetTransactions = channel.unary_unary(
            '/storage.Storage/GetTransactions',
            request_serializer=storage__pb2.GetTransactionsRequest.SerializeToString,
            response_deserializer=storage__pb2.GetTransactionsResponse.FromString,
        )
        self.GetLatestStateRoot = channel.unary_unary(
            '/storage.Storage/GetLatestStateRoot',
            request_serializer=storage__pb2.GetLatestStateRootRequest.SerializeToString,
            response_deserializer=storage__pb2.GetLatestStateRootResponse.FromString,
        )
        self.GetLatestAccountState = channel.unary_unary(
            '/storage.Storage/GetLatestAccountState',
            request_serializer=storage__pb2.GetLatestAccountStateRequest.SerializeToString,
            response_deserializer=storage__pb2.GetLatestAccountStateResponse.FromString,
        )
        self.GetAccountStateWithProofByVersion = channel.unary_unary(
            '/storage.Storage/GetAccountStateWithProofByVersion',
            request_serializer=storage__pb2.GetAccountStateWithProofByVersionRequest.SerializeToString,
            response_deserializer=storage__pb2.GetAccountStateWithProofByVersionResponse.FromString,
        )
        self.GetStartupInfo = channel.unary_unary(
            '/storage.Storage/GetStartupInfo',
            request_serializer=storage__pb2.GetStartupInfoRequest.SerializeToString,
            response_deserializer=storage__pb2.GetStartupInfoResponse.FromString,
        )
        self.GetEpochChangeLedgerInfos = channel.unary_unary(
            '/storage.Storage/GetEpochChangeLedgerInfos',
            request_serializer=storage__pb2.GetEpochChangeLedgerInfosRequest.SerializeToString,
            response_deserializer=validator__change__pb2.ValidatorChangeProof.FromString,
        )
        self.BackupAccountState = channel.unary_stream(
            '/storage.Storage/BackupAccountState',
            request_serializer=storage__pb2.BackupAccountStateRequest.SerializeToString,
            response_deserializer=storage__pb2.BackupAccountStateResponse.FromString,
        )
        self.GetAccountStateRangeProof = channel.unary_unary(
            '/storage.Storage/GetAccountStateRangeProof',
            request_serializer=storage__pb2.GetAccountStateRangeProofRequest.SerializeToString,
            response_deserializer=storage__pb2.GetAccountStateRangeProofResponse.FromString,
        )
        self.BackupTransaction = channel.unary_stream(
            '/storage.Storage/BackupTransaction',
            request_serializer=storage__pb2.BackupTransactionRequest.SerializeToString,
            response_deserializer=storage__pb2.BackupTransactionResponse.FromString,
        )
        self.BackupTransactionInfo = channel.unary_stream(
            '/storage.Storage/BackupTransactionInfo',
            request_serializer=storage__pb2.BackupTransactionInfoRequest.SerializeToString,
            response_deserializer=storage__pb2.BackupTransactionInfoResponse.FromString,
        )


class StorageServicer(object):
    """-----------------------------------------------------------------------------
    ---------------- Service definition for storage
    -----------------------------------------------------------------------------
    Write APIs.
    """

    def SaveTransactions(self, request, context):
        """Persist transactions. Called by Execution when either syncing nodes or
        committing blocks during normal operation.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateToLatestLedger(self, request, context):
        """Read APIs.

        Used to get a piece of data and return the proof of it. If the client
        knows and trusts a ledger info at version v, it should pass v in as the
        client_known_version and we will return the latest ledger info together
        with the proof that it derives from v.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetTransactions(self, request, context):
        """When we receive a request from a peer validator asking a list of
        transactions for state synchronization, this API can be used to serve the
        request. Note that the peer should specify a ledger version and all proofs
        in the response will be relative to this given ledger version.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetLatestStateRoot(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetLatestAccountState(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAccountStateWithProofByVersion(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetStartupInfo(self, request, context):
        """Returns information needed for libra core to start up.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetEpochChangeLedgerInfos(self, request, context):
        """Returns latest ledger infos per epoch.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BackupAccountState(self, request, context):
        """Returns a stream of account states.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAccountStateRangeProof(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BackupTransaction(self, request, context):
        """Returns a stream of transactions.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BackupTransactionInfo(self, request, context):
        """Returns a stream of transaction infos.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_StorageServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'SaveTransactions': grpc.unary_unary_rpc_method_handler(
            servicer.SaveTransactions,
            request_deserializer=storage__pb2.SaveTransactionsRequest.FromString,
            response_serializer=storage__pb2.SaveTransactionsResponse.SerializeToString,
        ),
        'UpdateToLatestLedger': grpc.unary_unary_rpc_method_handler(
            servicer.UpdateToLatestLedger,
            request_deserializer=get__with__proof__pb2.UpdateToLatestLedgerRequest.FromString,
            response_serializer=get__with__proof__pb2.UpdateToLatestLedgerResponse.SerializeToString,
        ),
        'GetTransactions': grpc.unary_unary_rpc_method_handler(
            servicer.GetTransactions,
            request_deserializer=storage__pb2.GetTransactionsRequest.FromString,
            response_serializer=storage__pb2.GetTransactionsResponse.SerializeToString,
        ),
        'GetLatestStateRoot': grpc.unary_unary_rpc_method_handler(
            servicer.GetLatestStateRoot,
            request_deserializer=storage__pb2.GetLatestStateRootRequest.FromString,
            response_serializer=storage__pb2.GetLatestStateRootResponse.SerializeToString,
        ),
        'GetLatestAccountState': grpc.unary_unary_rpc_method_handler(
            servicer.GetLatestAccountState,
            request_deserializer=storage__pb2.GetLatestAccountStateRequest.FromString,
            response_serializer=storage__pb2.GetLatestAccountStateResponse.SerializeToString,
        ),
        'GetAccountStateWithProofByVersion': grpc.unary_unary_rpc_method_handler(
            servicer.GetAccountStateWithProofByVersion,
            request_deserializer=storage__pb2.GetAccountStateWithProofByVersionRequest.FromString,
            response_serializer=storage__pb2.GetAccountStateWithProofByVersionResponse.SerializeToString,
        ),
        'GetStartupInfo': grpc.unary_unary_rpc_method_handler(
            servicer.GetStartupInfo,
            request_deserializer=storage__pb2.GetStartupInfoRequest.FromString,
            response_serializer=storage__pb2.GetStartupInfoResponse.SerializeToString,
        ),
        'GetEpochChangeLedgerInfos': grpc.unary_unary_rpc_method_handler(
            servicer.GetEpochChangeLedgerInfos,
            request_deserializer=storage__pb2.GetEpochChangeLedgerInfosRequest.FromString,
            response_serializer=validator__change__pb2.ValidatorChangeProof.SerializeToString,
        ),
        'BackupAccountState': grpc.unary_stream_rpc_method_handler(
            servicer.BackupAccountState,
            request_deserializer=storage__pb2.BackupAccountStateRequest.FromString,
            response_serializer=storage__pb2.BackupAccountStateResponse.SerializeToString,
        ),
        'GetAccountStateRangeProof': grpc.unary_unary_rpc_method_handler(
            servicer.GetAccountStateRangeProof,
            request_deserializer=storage__pb2.GetAccountStateRangeProofRequest.FromString,
            response_serializer=storage__pb2.GetAccountStateRangeProofResponse.SerializeToString,
        ),
        'BackupTransaction': grpc.unary_stream_rpc_method_handler(
            servicer.BackupTransaction,
            request_deserializer=storage__pb2.BackupTransactionRequest.FromString,
            response_serializer=storage__pb2.BackupTransactionResponse.SerializeToString,
        ),
        'BackupTransactionInfo': grpc.unary_stream_rpc_method_handler(
            servicer.BackupTransactionInfo,
            request_deserializer=storage__pb2.BackupTransactionInfoRequest.FromString,
            response_serializer=storage__pb2.BackupTransactionInfoResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'storage.Storage', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

 # This class is part of an EXPERIMENTAL API.


class Storage(object):
    """-----------------------------------------------------------------------------
    ---------------- Service definition for storage
    -----------------------------------------------------------------------------
    Write APIs.
    """

    @staticmethod
    def SaveTransactions(request,
                         target,
                         options=(),
                         channel_credentials=None,
                         call_credentials=None,
                         compression=None,
                         wait_for_ready=None,
                         timeout=None,
                         metadata=None):
        return grpc.experimental.unary_unary(request, target, '/storage.Storage/SaveTransactions',
                                             storage__pb2.SaveTransactionsRequest.SerializeToString,
                                             storage__pb2.SaveTransactionsResponse.FromString,
                                             options, channel_credentials,
                                             call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateToLatestLedger(request,
                             target,
                             options=(),
                             channel_credentials=None,
                             call_credentials=None,
                             compression=None,
                             wait_for_ready=None,
                             timeout=None,
                             metadata=None):
        return grpc.experimental.unary_unary(request, target, '/storage.Storage/UpdateToLatestLedger',
                                             get__with__proof__pb2.UpdateToLatestLedgerRequest.SerializeToString,
                                             get__with__proof__pb2.UpdateToLatestLedgerResponse.FromString,
                                             options, channel_credentials,
                                             call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetTransactions(request,
                        target,
                        options=(),
                        channel_credentials=None,
                        call_credentials=None,
                        compression=None,
                        wait_for_ready=None,
                        timeout=None,
                        metadata=None):
        return grpc.experimental.unary_unary(request, target, '/storage.Storage/GetTransactions',
                                             storage__pb2.GetTransactionsRequest.SerializeToString,
                                             storage__pb2.GetTransactionsResponse.FromString,
                                             options, channel_credentials,
                                             call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetLatestStateRoot(request,
                           target,
                           options=(),
                           channel_credentials=None,
                           call_credentials=None,
                           compression=None,
                           wait_for_ready=None,
                           timeout=None,
                           metadata=None):
        return grpc.experimental.unary_unary(request, target, '/storage.Storage/GetLatestStateRoot',
                                             storage__pb2.GetLatestStateRootRequest.SerializeToString,
                                             storage__pb2.GetLatestStateRootResponse.FromString,
                                             options, channel_credentials,
                                             call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetLatestAccountState(request,
                              target,
                              options=(),
                              channel_credentials=None,
                              call_credentials=None,
                              compression=None,
                              wait_for_ready=None,
                              timeout=None,
                              metadata=None):
        return grpc.experimental.unary_unary(request, target, '/storage.Storage/GetLatestAccountState',
                                             storage__pb2.GetLatestAccountStateRequest.SerializeToString,
                                             storage__pb2.GetLatestAccountStateResponse.FromString,
                                             options, channel_credentials,
                                             call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAccountStateWithProofByVersion(request,
                                          target,
                                          options=(),
                                          channel_credentials=None,
                                          call_credentials=None,
                                          compression=None,
                                          wait_for_ready=None,
                                          timeout=None,
                                          metadata=None):
        return grpc.experimental.unary_unary(request, target, '/storage.Storage/GetAccountStateWithProofByVersion',
                                             storage__pb2.GetAccountStateWithProofByVersionRequest.SerializeToString,
                                             storage__pb2.GetAccountStateWithProofByVersionResponse.FromString,
                                             options, channel_credentials,
                                             call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetStartupInfo(request,
                       target,
                       options=(),
                       channel_credentials=None,
                       call_credentials=None,
                       compression=None,
                       wait_for_ready=None,
                       timeout=None,
                       metadata=None):
        return grpc.experimental.unary_unary(request, target, '/storage.Storage/GetStartupInfo',
                                             storage__pb2.GetStartupInfoRequest.SerializeToString,
                                             storage__pb2.GetStartupInfoResponse.FromString,
                                             options, channel_credentials,
                                             call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetEpochChangeLedgerInfos(request,
                                  target,
                                  options=(),
                                  channel_credentials=None,
                                  call_credentials=None,
                                  compression=None,
                                  wait_for_ready=None,
                                  timeout=None,
                                  metadata=None):
        return grpc.experimental.unary_unary(request, target, '/storage.Storage/GetEpochChangeLedgerInfos',
                                             storage__pb2.GetEpochChangeLedgerInfosRequest.SerializeToString,
                                             validator__change__pb2.ValidatorChangeProof.FromString,
                                             options, channel_credentials,
                                             call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def BackupAccountState(request,
                           target,
                           options=(),
                           channel_credentials=None,
                           call_credentials=None,
                           compression=None,
                           wait_for_ready=None,
                           timeout=None,
                           metadata=None):
        return grpc.experimental.unary_stream(request, target, '/storage.Storage/BackupAccountState',
                                              storage__pb2.BackupAccountStateRequest.SerializeToString,
                                              storage__pb2.BackupAccountStateResponse.FromString,
                                              options, channel_credentials,
                                              call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAccountStateRangeProof(request,
                                  target,
                                  options=(),
                                  channel_credentials=None,
                                  call_credentials=None,
                                  compression=None,
                                  wait_for_ready=None,
                                  timeout=None,
                                  metadata=None):
        return grpc.experimental.unary_unary(request, target, '/storage.Storage/GetAccountStateRangeProof',
                                             storage__pb2.GetAccountStateRangeProofRequest.SerializeToString,
                                             storage__pb2.GetAccountStateRangeProofResponse.FromString,
                                             options, channel_credentials,
                                             call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def BackupTransaction(request,
                          target,
                          options=(),
                          channel_credentials=None,
                          call_credentials=None,
                          compression=None,
                          wait_for_ready=None,
                          timeout=None,
                          metadata=None):
        return grpc.experimental.unary_stream(request, target, '/storage.Storage/BackupTransaction',
                                              storage__pb2.BackupTransactionRequest.SerializeToString,
                                              storage__pb2.BackupTransactionResponse.FromString,
                                              options, channel_credentials,
                                              call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def BackupTransactionInfo(request,
                              target,
                              options=(),
                              channel_credentials=None,
                              call_credentials=None,
                              compression=None,
                              wait_for_ready=None,
                              timeout=None,
                              metadata=None):
        return grpc.experimental.unary_stream(request, target, '/storage.Storage/BackupTransactionInfo',
                                              storage__pb2.BackupTransactionInfoRequest.SerializeToString,
                                              storage__pb2.BackupTransactionInfoResponse.FromString,
                                              options, channel_credentials,
                                              call_credentials, compression, wait_for_ready, timeout, metadata)
