import logging
from web3 import Web3

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContractInteroperability:
    def __init__(self, provider_url):
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        logger.info("Connected to Ethereum provider.")

    def interact_with_contract(self, contract_address, contract_abi, function_name, *args):
        """Interact with a smart contract by calling a function."""
        try:
            contract = self.w3.eth.contract(address=contract_address, abi=contract_abi)
            function = getattr(contract.functions, function_name)
            result = function(*args).call()
            logger.info(f"Called {function_name} on contract {contract_address} with result: {result}")
            return result
        except Exception as e:
            logger.error(f"Error interacting with contract: {e}")
            raise

    def send_transaction(self, contract_address, contract_abi, function_name, private_key, *args):
        """Send a transaction to a smart contract function."""
        try:
            account = self.w3.eth.account.from_key(private_key)
            contract = self.w3.eth.contract(address=contract_address, abi=contract_abi)
            function = getattr(contract.functions, function_name)

            # Build the transaction
            transaction = function(*args).buildTransaction({
                'from': account.address,
                'nonce': self.w3.eth.getTransactionCount(account.address),
                'gas': 2000000,
                'gasPrice': self.w3.toWei('50', 'gwei')
            })

            # Sign the transaction
            signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key)

            # Send the transaction
            txn_hash = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
            logger.info(f"Transaction sent: {txn_hash.hex()}")
            return txn_hash.hex()
        except Exception as e:
            logger.error(f"Error sending transaction: {e}")
            raise

    def listen_to_events(self, contract_address, contract_abi, event_name):
        """Listen for events emitted by a smart contract."""
        try:
            contract = self.w3.eth.contract(address=contract_address, abi=contract_abi)
            event_filter = contract.events[event_name].createFilter(fromBlock='latest')

            logger.info(f"Listening for {event_name} events on contract {contract_address}...")
            while True:
                for event in event_filter.get_new_entries():
                    logger.info(f"New event: {event}")
        except Exception as e:
            logger.error(f"Error listening to events: {e}")
            raise

if __name__ == "__main__":
    provider_url = "https://your.ethereum.node"  # Replace with your Ethereum node URL
    contract_address = "0xYourContractAddress"  # Replace with the contract address
    contract_abi = json.loads('''[{"constant":true,"inputs":[],"name":"getData","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_data","type":"uint256"}],"name":"setData","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]''')  # Replace with the contract ABI

    # Initialize the contract interoperability
    interoperability = ContractInteroperability(provider_url)

    # Interact with the contract
    data = interoperability.interact_with_contract(contract_address, contract_abi, 'getData')
    print(f"Data from contract: {data}")

    # Send a transaction to set data
    private_key = "0xYourPrivateKey"  # Replace with your private key
    txn_hash = interoperability.send_transaction(contract_address, contract_abi, 'setData', private_key, 42)
    print(f"Transaction hash: {txn_hash}")

    # Listen for events (uncomment to use)
    # interoperability.listen_to_events(contract_address, contract_abi, 'YourEventName')
