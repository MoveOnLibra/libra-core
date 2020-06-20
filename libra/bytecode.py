from libra.transaction_scripts import bytecodes
from libra.hasher import HashValue

def get_transaction_name(code):
    for k, v in bytecodes.items():
        if code == v:
            return k + "_transaction"
    return "unknown transaction"


def get_script_name(code):
    for k, v in bytecodes.items():
        if code == v:
            return k
    return "script"


def get_script_name_by_hash(script_hash):
    if type(script_hash) == str:
        script_hash = bytes.fromhex(script_hash)
    for k, v in bytecodes.items():
        if HashValue.from_sha3_256(v) == script_hash:
            return k
    return "script"



def get_code_by_filename(script_file):
    with open(script_file, 'rb') as f:
        code = f.read()
        return code
