# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ticket.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cticket.proto\"O\n\x0bMedicamento\x12\x0c\n\x04name\x18\x01 \x02(\t\x12\x12\n\nquantidade\x18\x02 \x02(\x05\x12\x1e\n\x04tipo\x18\x03 \x02(\x0e\x32\x10.MedicamentoType\",\n\x06Ticket\x12\"\n\x0cmedicamentos\x18\x01 \x03(\x0b\x32\x0c.Medicamento*3\n\x0fMedicamentoType\x12\x08\n\x04NONE\x10\x00\x12\n\n\x06\x41MPOLA\x10\x01\x12\n\n\x06PACOTE\x10\x02')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ticket_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_MEDICAMENTOTYPE']._serialized_start=143
  _globals['_MEDICAMENTOTYPE']._serialized_end=194
  _globals['_MEDICAMENTO']._serialized_start=16
  _globals['_MEDICAMENTO']._serialized_end=95
  _globals['_TICKET']._serialized_start=97
  _globals['_TICKET']._serialized_end=141
# @@protoc_insertion_point(module_scope)
