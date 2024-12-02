import logging
import json
import os
from solcx import compile_source
from slither import Slither

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContractAuditor:
    def __init__(self, contract_source):
        self.contract_source = contract_source
        self.compiled_contract = None

    def compile_contract(self):
        """Compile the smart contract source code."""
        try:
            compiled_sol = compile_source(self.contract_source)
            contract_id, contract_interface = compiled_sol.popitem()
            self.compiled_contract = contract_interface
            logger.info("Contract compiled successfully.")
        except Exception as e:
            logger.error(f"Error compiling contract: {e}")
            raise

    def audit_contract(self):
        """Audit the smart contract for vulnerabilities."""
        if self.compiled_contract is None:
            raise Exception("Contract must be compiled before auditing.")

        # Save the contract source to a temporary file for Slither analysis
        temp_file_path = "temp_contract.sol"
        with open(temp_file_path, "w") as temp_file:
            temp_file.write(self.contract_source)

        # Run Slither for static analysis
        try:
            slither = Slither(temp_file_path)
            vulnerabilities = slither.get_vulnerabilities()
            logger.info("Audit completed. Found vulnerabilities:")
            for vulnerability in vulnerabilities:
                logger.info(f"- {vulnerability}")
        except Exception as e:
            logger.error(f"Error during auditing: {e}")
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

if __name__ == "__main__":
    # Sample Solidity contract source code
    contract_source = '''
    pragma solidity ^0.8.0;

    contract VulnerableContract {
        uint256 public balance;

        function deposit() public payable {
            balance += msg.value;
        }

        function withdraw(uint256 amount) public {
            require(amount <= balance, "Insufficient balance");
            payable(msg.sender).transfer(amount);
            balance -= amount;
        }
    }
    '''

    # Initialize the contract auditor
    auditor = ContractAuditor(contract_source)

    # Compile the contract
    auditor.compile_contract()

    # Audit the contract
    auditor.audit_contract()
