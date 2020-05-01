from libra.transaction_scripts import bytecodes


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


def get_code_by_filename(script_file):
    with open(script_file, 'rb') as f:
        code = f.read()
        return code
