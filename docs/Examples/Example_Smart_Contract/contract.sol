// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ExampleSmartContract {
    string public name;
    uint public value;

    constructor(string memory _name, uint _value) {
        name = _name;
        value = _value;
    }

    function setValue(uint _value) public {
        value = _value;
    }

    function getValue() public view returns (uint) {
        return value;
    }
}
