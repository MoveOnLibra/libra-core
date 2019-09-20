# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: consensus.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import ledger_info_pb2 as ledger__info__pb2
import transaction_pb2 as transaction__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='consensus.proto',
  package='network',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x0f\x63onsensus.proto\x12\x07network\x1a\x11ledger_info.proto\x1a\x11transaction.proto\"\x93\x02\n\x0c\x43onsensusMsg\x12%\n\x08proposal\x18\x01 \x01(\x0b\x32\x11.network.ProposalH\x00\x12\x1d\n\x04vote\x18\x02 \x01(\x0b\x32\r.network.VoteH\x00\x12.\n\rrequest_block\x18\x03 \x01(\x0b\x32\x15.network.RequestBlockH\x00\x12.\n\rrespond_block\x18\x04 \x01(\x0b\x32\x15.network.RespondBlockH\x00\x12*\n\x0btimeout_msg\x18\x05 \x01(\x0b\x32\x13.network.TimeoutMsgH\x00\x12&\n\tsync_info\x18\x06 \x01(\x0b\x32\x11.network.SyncInfoH\x00\x42\t\n\x07message\"X\n\x08Proposal\x12&\n\x0eproposed_block\x18\x01 \x01(\x0b\x32\x0e.network.Block\x12$\n\tsync_info\x18\x02 \x01(\x0b\x32\x11.network.SyncInfo\"a\n\x10PacemakerTimeout\x12\r\n\x05round\x18\x01 \x01(\x04\x12\x0e\n\x06\x61uthor\x18\x02 \x01(\x0c\x12\x11\n\tsignature\x18\x03 \x01(\x0c\x12\x1b\n\x04vote\x18\x04 \x01(\x0b\x32\r.network.Vote\"{\n\nTimeoutMsg\x12$\n\tsync_info\x18\x01 \x01(\x0b\x32\x11.network.SyncInfo\x12\x34\n\x11pacemaker_timeout\x18\x02 \x01(\x0b\x32\x19.network.PacemakerTimeout\x12\x11\n\tsignature\x18\x03 \x01(\x0c\"\xb2\x01\n\x08SyncInfo\x12\x30\n\x13highest_quorum_cert\x18\x01 \x01(\x0b\x32\x13.network.QuorumCert\x12\x30\n\x13highest_ledger_info\x18\x02 \x01(\x0b\x32\x13.network.QuorumCert\x12\x42\n\x14highest_timeout_cert\x18\x03 \x01(\x0b\x32$.network.PacemakerTimeoutCertificate\"Y\n\x1bPacemakerTimeoutCertificate\x12\r\n\x05round\x18\x01 \x01(\x04\x12+\n\x08timeouts\x18\x02 \x03(\x0b\x32\x19.network.PacemakerTimeout\"\xbc\x01\n\x05\x42lock\x12\n\n\x02id\x18\x01 \x01(\x0c\x12\x11\n\tparent_id\x18\x02 \x01(\x0c\x12\x0f\n\x07payload\x18\x03 \x01(\x0c\x12\r\n\x05round\x18\x04 \x01(\x04\x12\x0e\n\x06height\x18\x05 \x01(\x04\x12\x17\n\x0ftimestamp_usecs\x18\x06 \x01(\x04\x12(\n\x0bquorum_cert\x18\x07 \x01(\x0b\x32\x13.network.QuorumCert\x12\x0e\n\x06\x61uthor\x18\x08 \x01(\x0c\x12\x11\n\tsignature\x18\t \x01(\x0c\"o\n\nQuorumCert\x12$\n\tvote_data\x18\x01 \x01(\x0b\x32\x11.network.VoteData\x12;\n\x12signed_ledger_info\x18\x02 \x01(\x0b\x32\x1f.types.LedgerInfoWithSignatures\"\xba\x01\n\x08VoteData\x12\x10\n\x08\x62lock_id\x18\x01 \x01(\x0c\x12\x19\n\x11\x65xecuted_state_id\x18\x02 \x01(\x0c\x12\r\n\x05round\x18\x03 \x01(\x04\x12\x17\n\x0fparent_block_id\x18\x04 \x01(\x0c\x12\x1a\n\x12parent_block_round\x18\x05 \x01(\x04\x12\x1c\n\x14grandparent_block_id\x18\x06 \x01(\x0c\x12\x1f\n\x17grandparent_block_round\x18\x07 \x01(\x04\"w\n\x04Vote\x12$\n\tvote_data\x18\x01 \x01(\x0b\x32\x11.network.VoteData\x12\x0e\n\x06\x61uthor\x18\x02 \x01(\x0c\x12&\n\x0bledger_info\x18\x03 \x01(\x0b\x32\x11.types.LedgerInfo\x12\x11\n\tsignature\x18\x04 \x01(\x0c\"4\n\x0cRequestBlock\x12\x10\n\x08\x62lock_id\x18\x01 \x01(\x0c\x12\x12\n\nnum_blocks\x18\x02 \x01(\x04\"]\n\x0cRespondBlock\x12-\n\x06status\x18\x01 \x01(\x0e\x32\x1d.network.BlockRetrievalStatus\x12\x1e\n\x06\x62locks\x18\x02 \x03(\x0b\x32\x0e.network.Block*N\n\x14\x42lockRetrievalStatus\x12\r\n\tSUCCEEDED\x10\x00\x12\x10\n\x0cID_NOT_FOUND\x10\x01\x12\x15\n\x11NOT_ENOUGH_BLOCKS\x10\x02\x62\x06proto3')
  ,
  dependencies=[ledger__info__pb2.DESCRIPTOR,transaction__pb2.DESCRIPTOR,])

_BLOCKRETRIEVALSTATUS = _descriptor.EnumDescriptor(
  name='BlockRetrievalStatus',
  full_name='network.BlockRetrievalStatus',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SUCCEEDED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ID_NOT_FOUND', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NOT_ENOUGH_BLOCKS', index=2, number=2,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1693,
  serialized_end=1771,
)
_sym_db.RegisterEnumDescriptor(_BLOCKRETRIEVALSTATUS)

BlockRetrievalStatus = enum_type_wrapper.EnumTypeWrapper(_BLOCKRETRIEVALSTATUS)
SUCCEEDED = 0
ID_NOT_FOUND = 1
NOT_ENOUGH_BLOCKS = 2



_CONSENSUSMSG = _descriptor.Descriptor(
  name='ConsensusMsg',
  full_name='network.ConsensusMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='proposal', full_name='network.ConsensusMsg.proposal', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='vote', full_name='network.ConsensusMsg.vote', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='request_block', full_name='network.ConsensusMsg.request_block', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='respond_block', full_name='network.ConsensusMsg.respond_block', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timeout_msg', full_name='network.ConsensusMsg.timeout_msg', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sync_info', full_name='network.ConsensusMsg.sync_info', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='message', full_name='network.ConsensusMsg.message',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=67,
  serialized_end=342,
)


_PROPOSAL = _descriptor.Descriptor(
  name='Proposal',
  full_name='network.Proposal',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='proposed_block', full_name='network.Proposal.proposed_block', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sync_info', full_name='network.Proposal.sync_info', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=344,
  serialized_end=432,
)


_PACEMAKERTIMEOUT = _descriptor.Descriptor(
  name='PacemakerTimeout',
  full_name='network.PacemakerTimeout',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='round', full_name='network.PacemakerTimeout.round', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='author', full_name='network.PacemakerTimeout.author', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='signature', full_name='network.PacemakerTimeout.signature', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='vote', full_name='network.PacemakerTimeout.vote', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=434,
  serialized_end=531,
)


_TIMEOUTMSG = _descriptor.Descriptor(
  name='TimeoutMsg',
  full_name='network.TimeoutMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sync_info', full_name='network.TimeoutMsg.sync_info', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='pacemaker_timeout', full_name='network.TimeoutMsg.pacemaker_timeout', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='signature', full_name='network.TimeoutMsg.signature', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=533,
  serialized_end=656,
)


_SYNCINFO = _descriptor.Descriptor(
  name='SyncInfo',
  full_name='network.SyncInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='highest_quorum_cert', full_name='network.SyncInfo.highest_quorum_cert', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='highest_ledger_info', full_name='network.SyncInfo.highest_ledger_info', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='highest_timeout_cert', full_name='network.SyncInfo.highest_timeout_cert', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=659,
  serialized_end=837,
)


_PACEMAKERTIMEOUTCERTIFICATE = _descriptor.Descriptor(
  name='PacemakerTimeoutCertificate',
  full_name='network.PacemakerTimeoutCertificate',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='round', full_name='network.PacemakerTimeoutCertificate.round', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timeouts', full_name='network.PacemakerTimeoutCertificate.timeouts', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=839,
  serialized_end=928,
)


_BLOCK = _descriptor.Descriptor(
  name='Block',
  full_name='network.Block',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='network.Block.id', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='parent_id', full_name='network.Block.parent_id', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='payload', full_name='network.Block.payload', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='round', full_name='network.Block.round', index=3,
      number=4, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='height', full_name='network.Block.height', index=4,
      number=5, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp_usecs', full_name='network.Block.timestamp_usecs', index=5,
      number=6, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='quorum_cert', full_name='network.Block.quorum_cert', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='author', full_name='network.Block.author', index=7,
      number=8, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='signature', full_name='network.Block.signature', index=8,
      number=9, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=931,
  serialized_end=1119,
)


_QUORUMCERT = _descriptor.Descriptor(
  name='QuorumCert',
  full_name='network.QuorumCert',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='vote_data', full_name='network.QuorumCert.vote_data', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='signed_ledger_info', full_name='network.QuorumCert.signed_ledger_info', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1121,
  serialized_end=1232,
)


_VOTEDATA = _descriptor.Descriptor(
  name='VoteData',
  full_name='network.VoteData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='block_id', full_name='network.VoteData.block_id', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='executed_state_id', full_name='network.VoteData.executed_state_id', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='round', full_name='network.VoteData.round', index=2,
      number=3, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='parent_block_id', full_name='network.VoteData.parent_block_id', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='parent_block_round', full_name='network.VoteData.parent_block_round', index=4,
      number=5, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='grandparent_block_id', full_name='network.VoteData.grandparent_block_id', index=5,
      number=6, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='grandparent_block_round', full_name='network.VoteData.grandparent_block_round', index=6,
      number=7, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1235,
  serialized_end=1421,
)


_VOTE = _descriptor.Descriptor(
  name='Vote',
  full_name='network.Vote',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='vote_data', full_name='network.Vote.vote_data', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='author', full_name='network.Vote.author', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ledger_info', full_name='network.Vote.ledger_info', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='signature', full_name='network.Vote.signature', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1423,
  serialized_end=1542,
)


_REQUESTBLOCK = _descriptor.Descriptor(
  name='RequestBlock',
  full_name='network.RequestBlock',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='block_id', full_name='network.RequestBlock.block_id', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='num_blocks', full_name='network.RequestBlock.num_blocks', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1544,
  serialized_end=1596,
)


_RESPONDBLOCK = _descriptor.Descriptor(
  name='RespondBlock',
  full_name='network.RespondBlock',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='network.RespondBlock.status', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='blocks', full_name='network.RespondBlock.blocks', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1598,
  serialized_end=1691,
)

_CONSENSUSMSG.fields_by_name['proposal'].message_type = _PROPOSAL
_CONSENSUSMSG.fields_by_name['vote'].message_type = _VOTE
_CONSENSUSMSG.fields_by_name['request_block'].message_type = _REQUESTBLOCK
_CONSENSUSMSG.fields_by_name['respond_block'].message_type = _RESPONDBLOCK
_CONSENSUSMSG.fields_by_name['timeout_msg'].message_type = _TIMEOUTMSG
_CONSENSUSMSG.fields_by_name['sync_info'].message_type = _SYNCINFO
_CONSENSUSMSG.oneofs_by_name['message'].fields.append(
  _CONSENSUSMSG.fields_by_name['proposal'])
_CONSENSUSMSG.fields_by_name['proposal'].containing_oneof = _CONSENSUSMSG.oneofs_by_name['message']
_CONSENSUSMSG.oneofs_by_name['message'].fields.append(
  _CONSENSUSMSG.fields_by_name['vote'])
_CONSENSUSMSG.fields_by_name['vote'].containing_oneof = _CONSENSUSMSG.oneofs_by_name['message']
_CONSENSUSMSG.oneofs_by_name['message'].fields.append(
  _CONSENSUSMSG.fields_by_name['request_block'])
_CONSENSUSMSG.fields_by_name['request_block'].containing_oneof = _CONSENSUSMSG.oneofs_by_name['message']
_CONSENSUSMSG.oneofs_by_name['message'].fields.append(
  _CONSENSUSMSG.fields_by_name['respond_block'])
_CONSENSUSMSG.fields_by_name['respond_block'].containing_oneof = _CONSENSUSMSG.oneofs_by_name['message']
_CONSENSUSMSG.oneofs_by_name['message'].fields.append(
  _CONSENSUSMSG.fields_by_name['timeout_msg'])
_CONSENSUSMSG.fields_by_name['timeout_msg'].containing_oneof = _CONSENSUSMSG.oneofs_by_name['message']
_CONSENSUSMSG.oneofs_by_name['message'].fields.append(
  _CONSENSUSMSG.fields_by_name['sync_info'])
_CONSENSUSMSG.fields_by_name['sync_info'].containing_oneof = _CONSENSUSMSG.oneofs_by_name['message']
_PROPOSAL.fields_by_name['proposed_block'].message_type = _BLOCK
_PROPOSAL.fields_by_name['sync_info'].message_type = _SYNCINFO
_PACEMAKERTIMEOUT.fields_by_name['vote'].message_type = _VOTE
_TIMEOUTMSG.fields_by_name['sync_info'].message_type = _SYNCINFO
_TIMEOUTMSG.fields_by_name['pacemaker_timeout'].message_type = _PACEMAKERTIMEOUT
_SYNCINFO.fields_by_name['highest_quorum_cert'].message_type = _QUORUMCERT
_SYNCINFO.fields_by_name['highest_ledger_info'].message_type = _QUORUMCERT
_SYNCINFO.fields_by_name['highest_timeout_cert'].message_type = _PACEMAKERTIMEOUTCERTIFICATE
_PACEMAKERTIMEOUTCERTIFICATE.fields_by_name['timeouts'].message_type = _PACEMAKERTIMEOUT
_BLOCK.fields_by_name['quorum_cert'].message_type = _QUORUMCERT
_QUORUMCERT.fields_by_name['vote_data'].message_type = _VOTEDATA
_QUORUMCERT.fields_by_name['signed_ledger_info'].message_type = ledger__info__pb2._LEDGERINFOWITHSIGNATURES
_VOTE.fields_by_name['vote_data'].message_type = _VOTEDATA
_VOTE.fields_by_name['ledger_info'].message_type = ledger__info__pb2._LEDGERINFO
_RESPONDBLOCK.fields_by_name['status'].enum_type = _BLOCKRETRIEVALSTATUS
_RESPONDBLOCK.fields_by_name['blocks'].message_type = _BLOCK
DESCRIPTOR.message_types_by_name['ConsensusMsg'] = _CONSENSUSMSG
DESCRIPTOR.message_types_by_name['Proposal'] = _PROPOSAL
DESCRIPTOR.message_types_by_name['PacemakerTimeout'] = _PACEMAKERTIMEOUT
DESCRIPTOR.message_types_by_name['TimeoutMsg'] = _TIMEOUTMSG
DESCRIPTOR.message_types_by_name['SyncInfo'] = _SYNCINFO
DESCRIPTOR.message_types_by_name['PacemakerTimeoutCertificate'] = _PACEMAKERTIMEOUTCERTIFICATE
DESCRIPTOR.message_types_by_name['Block'] = _BLOCK
DESCRIPTOR.message_types_by_name['QuorumCert'] = _QUORUMCERT
DESCRIPTOR.message_types_by_name['VoteData'] = _VOTEDATA
DESCRIPTOR.message_types_by_name['Vote'] = _VOTE
DESCRIPTOR.message_types_by_name['RequestBlock'] = _REQUESTBLOCK
DESCRIPTOR.message_types_by_name['RespondBlock'] = _RESPONDBLOCK
DESCRIPTOR.enum_types_by_name['BlockRetrievalStatus'] = _BLOCKRETRIEVALSTATUS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ConsensusMsg = _reflection.GeneratedProtocolMessageType('ConsensusMsg', (_message.Message,), {
  'DESCRIPTOR' : _CONSENSUSMSG,
  '__module__' : 'consensus_pb2'
  # @@protoc_insertion_point(class_scope:network.ConsensusMsg)
  })
_sym_db.RegisterMessage(ConsensusMsg)

Proposal = _reflection.GeneratedProtocolMessageType('Proposal', (_message.Message,), {
  'DESCRIPTOR' : _PROPOSAL,
  '__module__' : 'consensus_pb2'
  # @@protoc_insertion_point(class_scope:network.Proposal)
  })
_sym_db.RegisterMessage(Proposal)

PacemakerTimeout = _reflection.GeneratedProtocolMessageType('PacemakerTimeout', (_message.Message,), {
  'DESCRIPTOR' : _PACEMAKERTIMEOUT,
  '__module__' : 'consensus_pb2'
  # @@protoc_insertion_point(class_scope:network.PacemakerTimeout)
  })
_sym_db.RegisterMessage(PacemakerTimeout)

TimeoutMsg = _reflection.GeneratedProtocolMessageType('TimeoutMsg', (_message.Message,), {
  'DESCRIPTOR' : _TIMEOUTMSG,
  '__module__' : 'consensus_pb2'
  # @@protoc_insertion_point(class_scope:network.TimeoutMsg)
  })
_sym_db.RegisterMessage(TimeoutMsg)

SyncInfo = _reflection.GeneratedProtocolMessageType('SyncInfo', (_message.Message,), {
  'DESCRIPTOR' : _SYNCINFO,
  '__module__' : 'consensus_pb2'
  # @@protoc_insertion_point(class_scope:network.SyncInfo)
  })
_sym_db.RegisterMessage(SyncInfo)

PacemakerTimeoutCertificate = _reflection.GeneratedProtocolMessageType('PacemakerTimeoutCertificate', (_message.Message,), {
  'DESCRIPTOR' : _PACEMAKERTIMEOUTCERTIFICATE,
  '__module__' : 'consensus_pb2'
  # @@protoc_insertion_point(class_scope:network.PacemakerTimeoutCertificate)
  })
_sym_db.RegisterMessage(PacemakerTimeoutCertificate)

Block = _reflection.GeneratedProtocolMessageType('Block', (_message.Message,), {
  'DESCRIPTOR' : _BLOCK,
  '__module__' : 'consensus_pb2'
  # @@protoc_insertion_point(class_scope:network.Block)
  })
_sym_db.RegisterMessage(Block)

QuorumCert = _reflection.GeneratedProtocolMessageType('QuorumCert', (_message.Message,), {
  'DESCRIPTOR' : _QUORUMCERT,
  '__module__' : 'consensus_pb2'
  # @@protoc_insertion_point(class_scope:network.QuorumCert)
  })
_sym_db.RegisterMessage(QuorumCert)

VoteData = _reflection.GeneratedProtocolMessageType('VoteData', (_message.Message,), {
  'DESCRIPTOR' : _VOTEDATA,
  '__module__' : 'consensus_pb2'
  # @@protoc_insertion_point(class_scope:network.VoteData)
  })
_sym_db.RegisterMessage(VoteData)

Vote = _reflection.GeneratedProtocolMessageType('Vote', (_message.Message,), {
  'DESCRIPTOR' : _VOTE,
  '__module__' : 'consensus_pb2'
  # @@protoc_insertion_point(class_scope:network.Vote)
  })
_sym_db.RegisterMessage(Vote)

RequestBlock = _reflection.GeneratedProtocolMessageType('RequestBlock', (_message.Message,), {
  'DESCRIPTOR' : _REQUESTBLOCK,
  '__module__' : 'consensus_pb2'
  # @@protoc_insertion_point(class_scope:network.RequestBlock)
  })
_sym_db.RegisterMessage(RequestBlock)

RespondBlock = _reflection.GeneratedProtocolMessageType('RespondBlock', (_message.Message,), {
  'DESCRIPTOR' : _RESPONDBLOCK,
  '__module__' : 'consensus_pb2'
  # @@protoc_insertion_point(class_scope:network.RespondBlock)
  })
_sym_db.RegisterMessage(RespondBlock)


# @@protoc_insertion_point(module_scope)
