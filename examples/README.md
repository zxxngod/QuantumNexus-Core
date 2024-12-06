# Basic Smart Contract

This is a simple smart contract written in Solidity that allows users to store and retrieve a message.

## Features

- Store a message
- Retrieve the stored message
- Update the message

## Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) (for development tools)
- [Truffle](https://www.trufflesuite.com/truffle) or [Hardhat](https://hardhat.org/) (for compiling and deploying)

### Installation

1. Clone the repository:
   ```bash
   1 git clone https://github.com/KOSASIH/QuantumNexus-Core.git
   2 cd examples/basic_smart_contract
   ```

2. Install dependencies:
   ```bash
   1 npm install
   ```
   
### Compilation
To compile the smart contract, run:

```bash
1 truffle compile
```

or

```bash
1 npx hardhat compile
```

### Deployment
To deploy the smart contract, run:

```bash
1 truffle migrate
```

or

```bash
1 npx hardhat run scripts/deploy.js
```

## Usage
After deployment, you can interact with the smart contract using the Truffle console or a web interface.

- **Set a message**:

```javascript
1 const contract = await BasicSmartContract.deployed();
2 await contract.setMessage("Hello, Quantum Nexus!");
```

- **Get the message**:

```javascript
1 const message = await contract.getMessage();
2 console.log(message); // Outputs: Hello, Quantum Nexus!
```

## License
This project is licensed under the MIT License.
