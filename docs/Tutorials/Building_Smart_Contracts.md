# Building Smart Contracts

In this tutorial, you will learn how to build smart contracts using the QuantumNexus-Core framework.

## Step 1: Create a New Smart Contract

Create a new file for your smart contract, e.g., `MyContract.sol`, and define your contract:

```solidity
1 pragma solidity ^0.8.0;
2 
3 contract MyContract {
4     uint public value;
5 
6     function setValue(uint _value) public {
7         value = _value;
8     }
9 }
```

## Step 2: Compile the Smart Contract
Use the QuantumNexus compiler to compile your smart contract:

```bash
1 nexus compile MyContract.sol
```

Step 3: Deploy the Smart Contract
Deploy your smart contract to the QuantumNexus network:

```bash
1 nexus deploy MyContract
```

Step 4: Interact with the Smart Contract
You can interact with your deployed smart contract using the API:

```bash
1 curl -X POST https://api.quantumnexus.com/api/smart_contracts/{contract_id}/setValue \
2 -H "Authorization: Bearer YOUR_API_KEY" \
3 -H "Content-Type: application/json" \
4 -d '{"value": 42}'
```

## Conclusion
You have successfully built and deployed a smart contract on QuantumNexus-Core! Explore more advanced features in the following tutorials.
