from libra.ledger_info import *
import libra
from datetime import datetime, timezone
import time
import pytest
#import pdb

def print_time_str(unix_timestamp):
    utc_time = datetime.fromtimestamp(unix_timestamp, timezone.utc)
    local_time = utc_time.astimezone()
    print(utc_time.strftime("%Y-%m-%d %H:%M:%S.%f%z (%Z)"))
    print(local_time.strftime("%Y-%m-%d %H:%M:%S.%f%z (%Z)"))
    return local_time

def time_offset_in_seconds():
    return -time.timezone

def test_time():
    assert time.localtime().tm_gmtoff == time_offset_in_seconds()
    utcnow = datetime.utcnow().timestamp()
    print_time_str(utcnow)
    now = datetime.now().timestamp()
    print_time_str(now)
    diff = (now - time_offset_in_seconds()) - utcnow
    assert diff > 0
    assert diff < 1
