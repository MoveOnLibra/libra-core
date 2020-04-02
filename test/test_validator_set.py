from libra.validator_set import ValidatorSet
from libra.account_config import AccountConfig


def test_validator_set_path():
    tag = ValidatorSet.tag()
    assert tag.address.hex() == AccountConfig.core_code_address()
    validator_set_path = '01ab28755a6fd52bd9423ed74554caa2b6ddc96234fb07d6dc089f05d919d9d726'
    assert ValidatorSet.resource_path() == bytes.fromhex(validator_set_path)

