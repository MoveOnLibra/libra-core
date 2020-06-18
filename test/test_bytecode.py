from libra.bytecode import get_script_name, get_transaction_name, get_code_by_filename
from libra.transaction_scripts import bytecodes


def check_bytecode(name):
    code = get_code_by_filename(f"transaction_scripts/{name}.mv")
    assert code == bytecodes[name]
    assert get_transaction_name(code) == f"{name}_transaction"

def test_get_code_by_filename():
    check_bytecode("mint")
    check_bytecode("peer_to_peer_with_metadata")
    check_bytecode("rotate_authentication_key")

def test_find_type():
    code = "a11ceb0b010007014600000004000000034a00000017000000046100000004000000056500000018000000077d0000005600000008d30000001000000009e3000000200000000000000101020001010101030203000104040101010005050101010006020602050a0200010501010305030a0204050a02030a02010900063c53454c463e0c4c696272614163636f756e74176372656174655f756e686f737465645f6163636f756e74066578697374731d7061795f66726f6d5f73656e6465725f776974685f6d65746164617461046d61696e00000000000000000000000000000000030000050d000a001101200305000508000a000a013d000a000a020b033d0102"
    name = get_transaction_name(bytes.fromhex(code))
    print(get_script_name(code))
