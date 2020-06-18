from libra.account import *
from libra.account_config import AccountConfig
from libra.json_print import json_print
#import pdb

def test_faucet_account(capsys):
    faucet_account = Account.gen_faucet_account(None)
    assert faucet_account.address_hex == AccountConfig.treasury_compliance_account_address()
    assert faucet_account.sequence_number == 0
    assert faucet_account.status == AccountStatus.Local
    assert faucet_account.public_key != faucet_account.auth_key
    json_print(faucet_account)
    assert capsys.readouterr().out == """{
    "address": "0000000000000000000000000b1e55ed",
    "private_key": "48942ab2b0b2d4a671bbb5a579b3dde8a2b303a548185899dd2ae4accdbd809d",
    "public_key": "340db4a117a835557b11c6f41962dc118df9b84d4ef78757614d77f4265ca210",
    "auth_key": "99d62d1c5bb90cee62c7eee5a6027bf0010054b89da104ab1c52b29f4eb60ab9"
}
"""
