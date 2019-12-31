# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: state_synchronizer.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='state_synchronizer.proto',
  package='state_synchronizer',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x18state_synchronizer.proto\x12\x12state_synchronizer\" \n\x0fGetChunkRequest\x12\r\n\x05\x62ytes\x18\x01 \x01(\x0c\"!\n\x10GetChunkResponse\x12\r\n\x05\x62ytes\x18\x01 \x01(\x0c\"\x9f\x01\n\x14StateSynchronizerMsg\x12<\n\rchunk_request\x18\x01 \x01(\x0b\x32#.state_synchronizer.GetChunkRequestH\x00\x12>\n\x0e\x63hunk_response\x18\x02 \x01(\x0b\x32$.state_synchronizer.GetChunkResponseH\x00\x42\t\n\x07messageb\x06proto3')
)




_GETCHUNKREQUEST = _descriptor.Descriptor(
  name='GetChunkRequest',
  full_name='state_synchronizer.GetChunkRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='bytes', full_name='state_synchronizer.GetChunkRequest.bytes', index=0,
      number=1, type=12, cpp_type=9, label=1,
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
  serialized_start=48,
  serialized_end=80,
)


_GETCHUNKRESPONSE = _descriptor.Descriptor(
  name='GetChunkResponse',
  full_name='state_synchronizer.GetChunkResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='bytes', full_name='state_synchronizer.GetChunkResponse.bytes', index=0,
      number=1, type=12, cpp_type=9, label=1,
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
  serialized_start=82,
  serialized_end=115,
)


_STATESYNCHRONIZERMSG = _descriptor.Descriptor(
  name='StateSynchronizerMsg',
  full_name='state_synchronizer.StateSynchronizerMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='chunk_request', full_name='state_synchronizer.StateSynchronizerMsg.chunk_request', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='chunk_response', full_name='state_synchronizer.StateSynchronizerMsg.chunk_response', index=1,
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
    _descriptor.OneofDescriptor(
      name='message', full_name='state_synchronizer.StateSynchronizerMsg.message',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=118,
  serialized_end=277,
)

_STATESYNCHRONIZERMSG.fields_by_name['chunk_request'].message_type = _GETCHUNKREQUEST
_STATESYNCHRONIZERMSG.fields_by_name['chunk_response'].message_type = _GETCHUNKRESPONSE
_STATESYNCHRONIZERMSG.oneofs_by_name['message'].fields.append(
  _STATESYNCHRONIZERMSG.fields_by_name['chunk_request'])
_STATESYNCHRONIZERMSG.fields_by_name['chunk_request'].containing_oneof = _STATESYNCHRONIZERMSG.oneofs_by_name['message']
_STATESYNCHRONIZERMSG.oneofs_by_name['message'].fields.append(
  _STATESYNCHRONIZERMSG.fields_by_name['chunk_response'])
_STATESYNCHRONIZERMSG.fields_by_name['chunk_response'].containing_oneof = _STATESYNCHRONIZERMSG.oneofs_by_name['message']
DESCRIPTOR.message_types_by_name['GetChunkRequest'] = _GETCHUNKREQUEST
DESCRIPTOR.message_types_by_name['GetChunkResponse'] = _GETCHUNKRESPONSE
DESCRIPTOR.message_types_by_name['StateSynchronizerMsg'] = _STATESYNCHRONIZERMSG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetChunkRequest = _reflection.GeneratedProtocolMessageType('GetChunkRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETCHUNKREQUEST,
  '__module__' : 'state_synchronizer_pb2'
  # @@protoc_insertion_point(class_scope:state_synchronizer.GetChunkRequest)
  })
_sym_db.RegisterMessage(GetChunkRequest)

GetChunkResponse = _reflection.GeneratedProtocolMessageType('GetChunkResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETCHUNKRESPONSE,
  '__module__' : 'state_synchronizer_pb2'
  # @@protoc_insertion_point(class_scope:state_synchronizer.GetChunkResponse)
  })
_sym_db.RegisterMessage(GetChunkResponse)

StateSynchronizerMsg = _reflection.GeneratedProtocolMessageType('StateSynchronizerMsg', (_message.Message,), {
  'DESCRIPTOR' : _STATESYNCHRONIZERMSG,
  '__module__' : 'state_synchronizer_pb2'
  # @@protoc_insertion_point(class_scope:state_synchronizer.StateSynchronizerMsg)
  })
_sym_db.RegisterMessage(StateSynchronizerMsg)


# @@protoc_insertion_point(module_scope)
