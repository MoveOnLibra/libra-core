import os, json
from os import listdir
from os.path import dirname

whitelists = [
    "add_validator",
    "remove_validator",
    "register_validator",
    "peer_to_peer",
    "peer_to_peer_with_metadata",
    "create_account",
    "mint",
    "rotate_authentication_key",
    "rotate_consensus_pubkey",
]

def all_scripts():
    curdir = dirname(__file__)
    return [f for f in listdir(curdir) if f.endswith(".mv")]

def get_code_by_filename(script_file):
    with open(script_file, 'rb') as f:
        code = f.read()
        return code


print("bytecodes = {")

for script in all_scripts():
    code = get_code_by_filename(f"transaction_scripts/{script}")
    script_name = script[0:0-len(".mv")]
    print(f"  '{script_name}' : {code},")

print("}")

