from libra.shell.libra_shell import *
from test_shell import prepare_shell, exec_input_with_client
from libra.account_address import Address
import libra
import pytest
import os, hashlib, random
from datetime import datetime
import pdb

try:
    os.environ['TESTNET_LOCAL']
    TESTNET_LOCAL = True
except KeyError:
    TESTNET_LOCAL = False


def test_move_compile_and_exec(capsys):
    if not TESTNET_LOCAL:
        return
    client, alias_to_cmd = prepare_shell(None)
    balance = client.grpc_client.get_balance("f1f48f56c4deea75f4393e832edef247547eb76e1cd498c27cc972073ec4dbde")
    exec_input_with_client("a r test/test.wallet", client, alias_to_cmd)
    exec_input_with_client("a mb 0 123", client, alias_to_cmd)
    exec_input_with_client("dev c 0 ../libra-client/test/pay_1.module.mvir module", client, alias_to_cmd)
    exec_input_with_client("dev p 0 ../libra-client/test/pay_1.module.mv", client, alias_to_cmd)
    exec_input_with_client("dev c 0 ../libra-client/test/use_pay.mvir script", client, alias_to_cmd)
    exec_input_with_client("dev e 0 ../libra-client/test/use_pay.mv  f1f48f56c4deea75f4393e832edef247547eb76e1cd498c27cc972073ec4dbde", client, alias_to_cmd)
    assert balance+1 == client.grpc_client.get_balance("f1f48f56c4deea75f4393e832edef247547eb76e1cd498c27cc972073ec4dbde")

def gen_random_address():
    hasher = hashlib.sha256()
    ran = random.random() + datetime.now().timestamp()
    hasher.update(ran.__str__().encode('utf-8'))
    return hasher.digest().hex()[0:64]

def test_no_blob_of_non_exsits_address():
    if not TESTNET_LOCAL:
        return
    with pytest.raises(libra.client.AccountError):
        libra.Client("testnet").get_account_state(gen_random_address())

def test_create_account_and_rotate_key():
    if not TESTNET_LOCAL:
        return
    wallet = libra.WalletLibrary.recover('test/test.wallet')
    assert wallet.child_count == 2
    a0 = wallet.accounts[0]
    c = libra.Client("testnet")
    wallet2 = libra.WalletLibrary.new()
    account = wallet2.new_account()
    address = account.address
    with pytest.raises(libra.client.AccountError):
        c.get_account_state(address)
    c.create_account(a0, address)
    #TODO: min gas required for txn: 600, gas submitted: 1
    account_resource = c.get_account_resource(address)
    assert account_resource.balance == 0
    assert account_resource.sequence_number == 0
    assert account_resource.sent_events.count == 0
    assert account_resource.received_events.count == 0
    assert Address.equal_address(account_resource.authentication_key, address)
    c.rotate_authentication_key(account, a0.public_key)
    account_resource = c.get_account_resource(address)
    assert account_resource.balance == 0
    assert account_resource.sequence_number == 1
    assert account_resource.sent_events.count == 0
    assert account_resource.received_events.count == 0
    assert bytes(account_resource.authentication_key) == a0.public_key
    # before rotate, authentication_key == address
    # after rotate,  authentication_key == public_key




