
def bail(hint, *args):
    errstr = hint.format(*args)
    raise AssertionError(errstr)

def ensure(exp, hint, *args):
    if not exp:
        bail(hint, *args)
