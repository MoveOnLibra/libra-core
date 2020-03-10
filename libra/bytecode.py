import json

bytecodes = {
    'add_validator' : b'\xa1\x1c\xeb\x0b\x01\x00\x07\x01F\x00\x00\x00\x04\x00\x00\x00\x03J\x00\x00\x00\x06\x00\x00\x00\x0cP\x00\x00\x00\x05\x00\x00\x00\rU\x00\x00\x00\x05\x00\x00\x00\x05Z\x00\x00\x00&\x00\x00\x00\x04\x80\x00\x00\x00 \x00\x00\x00\x07\xa0\x00\x00\x00\r\x00\x00\x00\x00\x00\x00\x02\x00\x01\x00\x01\x03\x00\x02\x00\x01\x05\x00\x03\x01\x05\x03\x00\x06<SELF>\x04main\x0bLibraSystem\radd_validator\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x03\x00\x0b\x00\x12\x01\x01\x02',

    'remove_validator' : b'\xa1\x1c\xeb\x0b\x01\x00\x07\x01F\x00\x00\x00\x04\x00\x00\x00\x03J\x00\x00\x00\x06\x00\x00\x00\x0cP\x00\x00\x00\x05\x00\x00\x00\rU\x00\x00\x00\x05\x00\x00\x00\x05Z\x00\x00\x00)\x00\x00\x00\x04\x83\x00\x00\x00 \x00\x00\x00\x07\xa3\x00\x00\x00\r\x00\x00\x00\x00\x00\x00\x02\x00\x01\x00\x01\x03\x00\x02\x00\x01\x05\x00\x03\x01\x05\x03\x00\x06<SELF>\x04main\x0bLibraSystem\x10remove_validator\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x03\x00\x0b\x00\x12\x01\x01\x02',

    'register_validator' : b'\xa1\x1c\xeb\x0b\x01\x00\x07\x01F\x00\x00\x00\x04\x00\x00\x00\x03J\x00\x00\x00\x06\x00\x00\x00\x0cP\x00\x00\x00\x10\x00\x00\x00\r`\x00\x00\x00\x10\x00\x00\x00\x05p\x00\x00\x009\x00\x00\x00\x04\xa9\x00\x00\x00 \x00\x00\x00\x07\xc9\x00\x00\x00\x17\x00\x00\x00\x00\x00\x00\x02\x00\x01\x00\x01\x03\x00\x02\x00\x06\x0b\x02\x0b\x02\x0b\x02\x0b\x02\x0b\x02\x0b\x02\x00\x03\x06\x0b\x02\x0b\x02\x0b\x02\x0b\x02\x0b\x02\x0b\x02\x03\x00\x06<SELF>\x04main\x0fValidatorConfig\x1cregister_candidate_validator\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\x00\x08\x00\x0b\x00\x0b\x01\x0b\x02\x0b\x03\x0b\x04\x0b\x05\x12\x01\x01\x02',

    'peer_to_peer_transfer' : b'\xa1\x1c\xeb\x0b\x01\x00\x07\x01F\x00\x00\x00\x04\x00\x00\x00\x03J\x00\x00\x00\x06\x00\x00\x00\x0cP\x00\x00\x00\x06\x00\x00\x00\rV\x00\x00\x00\x06\x00\x00\x00\x05\\\x00\x00\x00)\x00\x00\x00\x04\x85\x00\x00\x00 \x00\x00\x00\x07\xa5\x00\x00\x00\x0f\x00\x00\x00\x00\x00\x00\x02\x00\x01\x00\x01\x03\x00\x02\x00\x02\x05\x03\x00\x03\x02\x05\x03\x03\x00\x06<SELF>\x04main\x0cLibraAccount\x0fpay_from_sender\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x04\x00\x0b\x00\x0b\x01\x12\x01\x01\x02',

    'peer_to_peer_transfer_with_metadata' : b'\xa1\x1c\xeb\x0b\x01\x00\x07\x01F\x00\x00\x00\x04\x00\x00\x00\x03J\x00\x00\x00\x06\x00\x00\x00\x0cP\x00\x00\x00\x08\x00\x00\x00\rX\x00\x00\x00\x08\x00\x00\x00\x05`\x00\x00\x007\x00\x00\x00\x04\x97\x00\x00\x00 \x00\x00\x00\x07\xb7\x00\x00\x00\x11\x00\x00\x00\x00\x00\x00\x02\x00\x01\x00\x01\x03\x00\x02\x00\x03\x05\x03\x0b\x02\x00\x03\x03\x05\x03\x0b\x02\x03\x00\x06<SELF>\x04main\x0cLibraAccount\x1dpay_from_sender_with_metadata\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x05\x00\x0b\x00\x0b\x01\x0b\x02\x12\x01\x01\x02',

    'create_account' : b'\xa1\x1c\xeb\x0b\x01\x00\x07\x01F\x00\x00\x00\x04\x00\x00\x00\x03J\x00\x00\x00\x06\x00\x00\x00\x0cP\x00\x00\x00\x06\x00\x00\x00\rV\x00\x00\x00\x06\x00\x00\x00\x05\\\x00\x00\x00,\x00\x00\x00\x04\x88\x00\x00\x00 \x00\x00\x00\x07\xa8\x00\x00\x00\x0f\x00\x00\x00\x00\x00\x00\x02\x00\x01\x00\x01\x03\x00\x02\x00\x02\x05\x03\x00\x03\x02\x05\x03\x03\x00\x06<SELF>\x04main\x0cLibraAccount\x12create_new_account\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x04\x00\x0b\x00\x0b\x01\x12\x01\x01\x02',

    'mint' : b'\xa1\x1c\xeb\x0b\x01\x00\x07\x01F\x00\x00\x00\x04\x00\x00\x00\x03J\x00\x00\x00\x06\x00\x00\x00\x0cP\x00\x00\x00\x06\x00\x00\x00\rV\x00\x00\x00\x06\x00\x00\x00\x05\\\x00\x00\x00)\x00\x00\x00\x04\x85\x00\x00\x00 \x00\x00\x00\x07\xa5\x00\x00\x00\x0f\x00\x00\x00\x00\x00\x00\x02\x00\x01\x00\x01\x03\x00\x02\x00\x02\x05\x03\x00\x03\x02\x05\x03\x03\x00\x06<SELF>\x04main\x0cLibraAccount\x0fmint_to_address\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x04\x00\x0b\x00\x0b\x01\x12\x01\x01\x02',

    'rotate_authentication_key' : b'\xa1\x1c\xeb\x0b\x01\x00\x07\x01F\x00\x00\x00\x04\x00\x00\x00\x03J\x00\x00\x00\x06\x00\x00\x00\x0cP\x00\x00\x00\x06\x00\x00\x00\rV\x00\x00\x00\x06\x00\x00\x00\x05\\\x00\x00\x003\x00\x00\x00\x04\x8f\x00\x00\x00 \x00\x00\x00\x07\xaf\x00\x00\x00\r\x00\x00\x00\x00\x00\x00\x02\x00\x01\x00\x01\x03\x00\x02\x00\x01\x0b\x02\x00\x03\x01\x0b\x02\x03\x00\x06<SELF>\x04main\x0cLibraAccount\x19rotate_authentication_key\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x03\x00\x0b\x00\x12\x01\x01\x02',

    'rotate_consensus_pubkey' : b'\xa1\x1c\xeb\x0b\x01\x00\x07\x01F\x00\x00\x00\x04\x00\x00\x00\x03J\x00\x00\x00\x06\x00\x00\x00\x0cP\x00\x00\x00\x06\x00\x00\x00\rV\x00\x00\x00\x06\x00\x00\x00\x05\\\x00\x00\x004\x00\x00\x00\x04\x90\x00\x00\x00 \x00\x00\x00\x07\xb0\x00\x00\x00\r\x00\x00\x00\x00\x00\x00\x02\x00\x01\x00\x01\x03\x00\x02\x00\x01\x0b\x02\x00\x03\x01\x0b\x02\x03\x00\x06<SELF>\x04main\x0fValidatorConfig\x17rotate_consensus_pubkey\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x03\x00\x0b\x00\x12\x01\x01\x02',
}


def get_transaction_name(code):
    for k, v in bytecodes.items():
        if code == v:
            return k+"_transaction"
    return "unknown transaction"



def get_code_by_jsonfile(script_file):
    with open(script_file) as f:
        amap = json.load(f)
        return bytes(amap['code'])


def get_code_by_filename(script_file):
    with open(script_file, 'rb') as f:
        code = f.read()
        return code