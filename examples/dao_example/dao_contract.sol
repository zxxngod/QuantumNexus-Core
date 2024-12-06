// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleDAO {
    struct Proposal {
        string description;
        uint256 voteCount;
        mapping(address => bool) voters;
    }

    address public owner;
    Proposal[] public proposals;

    event ProposalCreated(uint256 proposalId, string description);
    event Voted(uint256 proposalId, address voter);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can perform this action");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function createProposal(string memory description) public onlyOwner {
        Proposal storage newProposal = proposals.push();
        newProposal.description = description;
        newProposal.voteCount = 0;
        emit ProposalCreated(proposals.length - 1, description);
    }

    function vote(uint256 proposalId) public {
        Proposal storage proposal = proposals[proposalId];
        require(!proposal.voters[msg.sender], "You have already voted");
        
        proposal.voters[msg.sender] = true;
        proposal.voteCount += 1;
        emit Voted(proposalId, msg.sender);
    }

    function getProposal(uint256 proposalId) public view returns (string memory description, uint256 voteCount) {
        Proposal storage proposal = proposals[proposalId];
        return (proposal.description, proposal.voteCount);
    }

    function getProposalCount() public view returns (uint256) {
        return proposals.length;
    }
}
