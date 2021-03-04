from ecdsa import SECP256k1, SigningKey

from blockchain import Blockchain, Transaction

if __name__ == "__main__":
    my_sk = SigningKey.from_string(
        bytes.fromhex(
            "e692071a67f14a9ad2ca534c27e7e46486d1297dd6bcc30d67fe573bb66e121a"
        ),
        curve=SECP256k1,
    )
    my_vk = my_sk.verifying_key.to_string().hex()

    cycoin = Blockchain()

    tx_1 = Transaction(my_vk, "public key goes here", 10)
    tx_1.sign_transaction(my_sk)

    cycoin.add_transaction(tx_1)

    print("START MINING")
    cycoin.mine_pending_transactions(my_vk)

    print("DONE MINING")
    print("my balance: ", cycoin.get_balance_of_address(my_vk))

    cycoin.print_chain()
