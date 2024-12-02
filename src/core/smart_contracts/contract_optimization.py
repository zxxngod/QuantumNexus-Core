import logging
from web3 import Web3
from solcx import compile_source

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContractOptimizer:
    def __init__(self, provider_url, contract_source):
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        self.contract_source = contract_source
        self.compiled_contract = None

    def compile_contract(self, optimize=True):
        """Compile the smart contract source code with optimization settings."""
        try:
            compiled_sol = compile_source(
                self.contract_source,
                optimize=optimize
            )
            contract_id, contract_interface = compiled_sol.popitem()
            self.compiled_contract = contract_interface
            logger.info("Contract compiled successfully with optimization.")
        except Exception as e:
            logger.error(f"Error compiling contract: {e}")
            raise

    def estimate_gas(self, function_name, *args):
        """Estimate the gas required for a function call."""
        if self.compiled_contract is None:
            raise Exception("Contract must be compiled before estimating gas.")

        contract = self.w3.eth.contract(
            abi=self.compiled_contract['abi'],
            bytecode=self.compiled_contract['bin']
        )
        function = getattr(contract.functions, function_name)

        # Build the transaction for gas estimation
        transaction = function(*args).buildTransaction({
            'from': self.w3.eth.defaultAccount,
            'gas': 2000000,
            'gasPrice': self.w3.toWei('50', 'gwei')
        })

        # Estimate gas
        try:
            gas_estimate = self.w3.eth.estimateGas(transaction)
            logger.info(f"Estimated gas for function '{function_name}': {gas_estimate}")
            return gas_estimate
        except Exception as e:
            logger.error(f"Error estimating gas for function '{function_name}': {e}")
            raise

if __name__ == "__main__":
    provider_url = "https://your.ethereum.node"  # Replace with your Ethereum node URL

    # Sample Solidity contract source code
    contract_source = '''
    pragma solidity ^0.8.0;

    contract SimpleStorage {
        uint256 private data;

        function setData(uint256 _data) public {
            data = _data;
        }

        function getData() public view returns (uint256) {
            return data;
        }
    }
    '''

    # Initialize the contract optimizer
    optimizer = ContractOptimizer(provider_url, contract_source)

    # Compile the contract with optimization
    optimizer.compile_contract(optimize=True)

    # Estimate gas for setting data
    gas_for_set_data = optimizer.estimate_gas('setData', 42)
    print(f"Estimated gas for setData: {gas_for_set_data}")

    # Estimate gas for getting data
    gas_for_get_data = optimizer.estimate_gas('getData')
    print(f"Estimated gas for getData: {gas_for_get_data}")
