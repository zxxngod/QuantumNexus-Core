# Simple DAO Example

This is a simple Decentralized Autonomous Organization (DAO) smart contract written in Solidity. It allows the owner to create proposals and enables users to vote on those proposals.

## Features

- Create proposals
- Vote on proposals
- Retrieve proposal details
- Count the number of proposals

## Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) (for development tools)
- [Truffle](https://www.trufflesuite.com/truffle) or [Hardhat](https://hardhat.org/) (for compiling and deploying)
- [Ganache](https://www.trufflesuite.com/ganache) (for local blockchain testing)

### Installation

1. Clone the repository:
   ```bash
   1 git clone https://github.com/KOSASIH/QuantumNexus-Core.git
   2 cd examples/dao_example
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

- Create a proposal:

```javascript
1 const dao = await SimpleDAO.deployed();
2 await dao.createProposal("Proposal for new feature");
```

- Vote on a proposal:

```javascript
1 await dao.vote(0); // Vote on the first proposal
```

- Get proposal details:

```javascript
1 const proposal = await dao.getProposal(0);
2 console.log(`Description: ${proposal[0]}, Vote Count: ${proposal[1]}`);
```

- Get the total number of proposals:

```javascript
1 const count = await dao.getProposalCount();
2 console.log(`Total Proposals: ${count}`);
```

## License
This project is licensed under the MIT License.
