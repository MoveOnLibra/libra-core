from libra.account import *
from libra.account_config import AccountConfig
from libra.json_print import json_print
#import pdb

def test_faucet_account(capsys):
    faucet_account = Account.gen_faucet_account(None)
    assert faucet_account.address_hex == AccountConfig.association_address()
    assert faucet_account.sequence_number == 0
    assert faucet_account.status == AccountStatus.Local
    assert faucet_account.public_key != faucet_account.auth_key
    json_print(faucet_account)
    assert capsys.readouterr().out == """{
    "address": "0000000000000000000000000a550c18",
    "private_key": "99622b3e626182ca29cc0c759d4f639b97ad1cee5ec12cab2c9c0d1120c6f8e7",
    "public_key": "78153472e480e0222ce49ac048e9c915bcfb4e469cb3888d69da30f653a911b9",
    "auth_key": "5ce7f497ed9d5959fede6f73c4a5b53144a8a4a631a7faf6fdfe390f55688f2e"
}
"""
