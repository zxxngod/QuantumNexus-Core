import hashlib
import time
import random
from collections import defaultdict

class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        value = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}{self.nonce}".encode()
        return hashlib.sha256(value).hexdigest()

class ProofOfWork:
    def __init__(self, difficulty):
        self.difficulty = difficulty

    def mine_block(self, block):
        while block.hash[:self.difficulty] != '0' * self.difficulty:
            block.nonce += 1
            block.hash = block.calculate_hash()
        return block

class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.chain = []
        self.difficulty = 4  # Example difficulty
        self.pow = ProofOfWork(self.difficulty)

    def create_genesis_block(self):
        genesis_block = Block(0, "0", time.time(), "Genesis Block")
        self.chain.append(genesis_block)

    def add_block(self, data):
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), previous_block.hash, time.time(), data)
        mined_block = self.pow.mine_block(new_block)
        self.chain.append(mined_block)
        return mined_block

class PBFTNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.chain = []
        self.prepared = defaultdict(int)
        self.committed = defaultdict(int)

    def create_genesis_block(self):
        genesis_block = Block(0, "0", time.time(), "Genesis Block")
        self.chain.append(genesis_block)

    def propose_block(self, data):
        proposed_block = Block(len(self.chain), self.chain[-1].hash, time.time(), data)
        return proposed_block

    def prepare_block(self, proposed_block):
        self.prepared[proposed_block.hash] += 1
        if self.prepared[proposed_block.hash] > 2:  # Simple majority
            self.commit_block(proposed_block)

    def commit_block(self, proposed_block):
        self.chain.append(proposed_block)
        print(f"Node {self.node_id} committed block: {proposed_block.hash}")

class Blockchain:
    def __init__(self):
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)

    def create_genesis_blocks(self):
        for node in self.nodes:
            node.create_genesis_block()

    def simulate_pow(self, data):
        for node in self.nodes:
            node.add_block(data)
            print(f"Node {node.node_id} mined block: {node.chain[-1].hash}")

    def simulate_pbft(self, data):
        for node in self.nodes:
            proposed_block = node.propose_block(data)
            for n in self.nodes:
                n.prepare_block(proposed_block)

if __name__ == "__main__":
    # Example usage of the consensus mechanisms
    blockchain = Blockchain()

    # Create nodes
    for i in range(3):
        node = Node(i)
        blockchain.add_node(node)

    # Create genesis blocks
    blockchain.create_genesis_blocks()

    # Simulate Proof of Work
    blockchain.simulate_pow("Block 1 Data")
    blockchain.simulate_pow("Block 2 Data")

    # Create PBFT nodes
    pbft_blockchain = Blockchain()
    for i in range(3):
        pbft_node = PBFTNode(i)
        pbft_blockchain.add_node(pbft_node)

    # Create genesis blocks for PBFT
    pbft_blockchain.create_genesis_blocks()

    # Simulate Practical Byzantine Fault Tolerance
    pbft_blockchain.simulate_pbft("PBFT Block 1 Data")
