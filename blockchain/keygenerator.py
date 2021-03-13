from ecdsa import SECP256k1, SigningKey

sk = SigningKey.generate(curve=SECP256k1)
vk = sk.verifying_key

sk_string = sk.to_string().hex()
vk_string = vk.to_string().hex()

print("signing_key:", sk_string)
print("verifying_key:", vk_string)
