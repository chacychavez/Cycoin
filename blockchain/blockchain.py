import time
from hashlib import sha256

from ecdsa import SECP256k1, VerifyingKey


class Transaction:
    def __init__(self, from_address, to_address, amount):
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount

    def calculate_hash(self):
        return sha256(
            (self.from_address + self.to_address + str(self.amount)).encode("utf-8")
        ).hexdigest()

    def sign_transaction(self, signing_key):
        if signing_key.verifying_key.to_string().hex() != self.from_address:
            raise Exception("You cannot sign transaction for other wallet!")

        hash_tx = self.calculate_hash()
        sig = signing_key.sign(bytes.fromhex(hash_tx))
        self.signature = sig.hex()

    def is_valid(self):
        if self.from_address == None:
            return True

        if self.signature is None:
            raise Exception("No signature in this transaction!")

        verifiying_key = VerifyingKey.from_string(
            bytes.fromhex(self.from_address), curve=SECP256k1
        )
        return verifiying_key.verify(
            bytes.fromhex(self.signature), bytes.fromhex(self.calculate_hash())
        )


class Block:
    def __init__(self, timestamp, transactions, previous_hash=""):
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return sha256(
            (
                self.previous_hash
                + str(self.timestamp)
                + str(self.transactions)
                + str(self.nonce)
            ).encode("utf-8")
        ).hexdigest()

    # proof-of-work
    # secure blockchain against spamming and tampering
    def mine_block(self, difficulty):
        while self.hash[0:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

        print("block mined: " + self.hash)

    def has_valid_transactions(self):
        for tx in self.transactions:
            if not tx.is_valid():
                return False

        return True

    def get_transactions(self):
        return self.transactions


class Blockchain:
    def __init__(self):
        self.chain = [self._create_genesis_block()]
        self.difficulty = 2
        self.pending_transactions = []
        self.mining_reward = 100

    def _create_genesis_block(self):
        return Block(time.time(), None, "0")

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if not current_block.has_valid_transactions():
                return False

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def get_latest_block(self):
        return self.chain[-1]

    def mine_pending_transactions(self, mining_reward_address):
        # XXX: It will continue mining even if there is no pending_transactions.
        reward_tx = Transaction(None, mining_reward_address, self.mining_reward)
        self.pending_transactions.append(reward_tx)

        block = Block(time.time(), self.pending_transactions)
        block.mine_block(self.difficulty)

        block.previous_hash = self.chain[-1].hash
        self.chain.append(block)

        self.pending_transactions = []

    def add_transaction(self, transaction):
        if transaction.from_address is None or transaction.to_address is None:
            raise Exception("Transaction must include from and to address!")

        if not transaction.is_valid():
            raise Exception("Cannot add invalid transaction to the chain!")

        self.pending_transactions.append(transaction)

    def get_balance_of_address(self, address):
        balance = 0

        for block in self.chain:
            if block.transactions:
                for transaction in block.transactions:
                    if address == transaction.from_address:
                        balance -= transaction.amount
                    if address == transaction.to_address:
                        balance += transaction.amount

        return balance

    def get_chain(self):
        return self.chain

    def get_transactions(self, block_hash):
        for block in self.chain:
            print(block)
            if block.hash == block_hash:
                return block.get_transactions()
        return []

