# Example Smart Contract

This example demonstrates a simple smart contract written in Solidity.

## Overview

The `ExampleSmartContract` allows you to set and get a value, along with storing a name.

## Functions

- `constructor(string memory _name, uint _value)`: Initializes the contract with a name and a value.
- `setValue(uint _value)`: Sets a new value.
- `getValue()`: Returns the current value.

## Deployment

To deploy this contract, use the QuantumNexus deployment tools:

```bash
1 nexus deploy ExampleSmartContract
```
