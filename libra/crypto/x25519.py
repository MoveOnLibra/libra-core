from canoser import BytesT, DelegateT

# The length of the DHPublicKey
X25519_PUBLIC_KEY_LENGTH = 32

# The length of the DHPrivateKey
X25519_PRIVATE_KEY_LENGTH = 32


class X25519PrivateKey(DelegateT):
    delegate_type = BytesT(X25519_PRIVATE_KEY_LENGTH)


class X25519PublicKey(DelegateT):
    delegate_type = BytesT(X25519_PUBLIC_KEY_LENGTH)
