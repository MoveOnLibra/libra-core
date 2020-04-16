from libra.validator_config import *
import pytest

def test_validator_config():
    assert ValidatorConfigResource.struct_identifier() == ValidatorConfigResource.STRUCT_NAME
    assert ValidatorConfigResource.type_params() == []
    assert ValidatorConfigResource.struct_tag().module == ValidatorConfigResource.MODULE_NAME
    assert ValidatorConfigResource.struct_tag().name == ValidatorConfigResource.STRUCT_NAME

