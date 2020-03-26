from libra.validator_set import ValidatorSet
from libra.account_config import AccountConfig


def test_validator_set_path():
    tag = ValidatorSet.validator_set_tag()
    assert tag.address.hex() == AccountConfig.core_code_address()
    validator_set_path = '0185d17846384ab356223035eef279974ca0d158352fe96c28ebc620f3beb417f5'
    assert ValidatorSet.validator_set_path() == bytes.fromhex(validator_set_path)

