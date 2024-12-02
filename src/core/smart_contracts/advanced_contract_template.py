from web3 import Web3
from solcx import compile_source
import json

class AdvancedSmartContract:
    def __init__(self, provider_url, contract_source):
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        self.contract_source = contract_source
        self.contract = None
        self.contract_address = None
        self.account = None

    def set_account(self, private_key):
        """Set the account for transactions."""
        self.account = self.w3.eth.account.from_key(private_key)

    def compile_contract(self):
        """Compile the smart contract source code."""
        compiled_sol = compile_source(self.contract_source)
        contract_id, contract_interface = compiled_sol.popitem()
        self.contract = self.w3.eth.contract(
            address=self.contract_address,
            abi=contract_interface['abi']
        )
        return contract_interface

    def deploy_contract(self):
        """Deploy the smart contract to the Ethereum network."""
        if self.contract is None:
            raise Exception("Contract must be compiled before deployment.")

        contract_constructor = self.contract.constructor()
        transaction = contract_constructor.buildTransaction({
            'from': self.account.address,
            'nonce': self.w3.eth.getTransactionCount(self.account.address),
            'gas': 2000000,
            'gasPrice': self.w3.toWei('50', 'gwei')
        })

        signed_txn = self.w3.eth.account.signTransaction(transaction, self.account.privateKey)
        tx_hash = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        self.contract_address = tx_receipt.contractAddress
        print(f"Contract deployed at address: {self.contract_address}")

    def call_function(self, function_name, *args):
        """Call a function of the smart contract."""
        if self.contract is None:
            raise Exception("Contract must be compiled before calling functions.")

        function = getattr(self.contract.functions, function_name)
        return function(*args).call()

    def send_transaction(self, function_name, *args):
        """Send a transaction to a function of the smart contract."""
        if self.contract is None:
            raise Exception("Contract must be compiled before sending transactions.")

        function = getattr(self.contract.functions, function_name)
        transaction = function(*args).buildTransaction({
            'from': self.account.address,
            'nonce': self.w3.eth.getTransactionCount(self.account.address),
            'gas': 2000000,
            'gasPrice': self.w3.toWei('50', 'gwei')
        })

        signed_txn = self.w3.eth.account.signTransaction(transaction, self.account.privateKey)
        tx_hash = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        return tx_receipt

    def get_contract_info(self):
        """Retrieve contract information."""
        return {
            "address": self.contract_address,
            "abi": json.dumps(self.contract.abi)
        }

if __name__ == "__main__":
    provider_url = "https://your.ethereum.node"  # Replace with your Ethereum node URL
    private_key = "your_private_key"  # Replace with your Ethereum account private key

    # Sample Solidity contract source code
    contract_source = '''
    pragma solidity ^0.8.0;

    contract AdvancedStorage {
        uint256 number;

 function set(uint256 num) public {
            number = num;
        }

        function get() public view returns (uint256) {
            return number;
        }

        function increment() public {
            number += 1;
        }

        function decrement() public {
            require(number > 0, "Number must be greater than zero");
            number -= 1;
        }
    }
    '''

    # Initialize the advanced smart contract
    advanced_smart_contract = AdvancedSmartContract(provider_url, contract_source)
    advanced_smart_contract.set_account(private_key)

    # Compile the contract
    advanced_smart_contract.compile_contract()

    # Deploy the contract
    advanced_smart_contract.deploy_contract()

    # Interact with the contract
    advanced_smart_contract.send_transaction('set', 42)
    value = advanced_smart_contract.call_function('get')
    print(f"Stored value: {value}")

    # Increment the stored value
    advanced_smart_contract.send_transaction('increment')
    incremented_value = advanced_smart_contract.call_function('get')
    print(f"Incremented value: {incremented_value}")

    # Decrement the stored value
    advanced_smart_contract.send_transaction('decrement')
    decremented_value = advanced_smart_contract.call_function('get')
    print(f"Decremented value: {decremented_value}")

    # Retrieve contract information
    contract_info = advanced_smart_contract.get_contract_info()
    print(f"Contract Address: {contract_info['address']}")
    print(f"Contract ABI: {contract_info['abi']}")
