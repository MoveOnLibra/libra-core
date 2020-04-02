
class MempoolAddTransactionStatusCode:

    @classmethod
    def get_name(cls, status):
        for name, code in cls.__dict__.items():
            if code == status:
                return name
        raise f"mempool error code:{status} not exsits."

    # Transaction was accepted by Mempool
    Accepted = 0
    # Sequence number is old, etc.
    InvalidSeqNumber = 1
    # Mempool is full (reached max global capacity)
    MempoolIsFull = 2
    # Account reached max capacity per account
    TooManyTransactions = 3
    # Invalid update. Only gas price increase is allowed
    InvalidUpdate = 4
    # transaction didn't pass vm_validation
    VmError = 5
    UnknownStatus = 6