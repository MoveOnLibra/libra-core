from libra.account_address import ADDRESS_LENGTH
from libra.validator_verifier import ValidatorVerifier
#import pdb


def test_empty_validator():
    validator_verifier = ValidatorVerifier({})
    assert len(validator_verifier.address_to_validator_info) == 0
    assert validator_verifier.quorum_voting_power == 0
    assert validator_verifier.total_voting_power == 0
