// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract ModelRegistry {

    struct Model {
        string name;
        string version;
        string hash;
        uint256 timestamp;
    }

    mapping(uint256 => Model) public models;
    uint256 public modelCount;

    function registerModel(
        string memory name,
        string memory version,
        string memory hash
    ) public {

        modelCount++;

        models[modelCount] = Model(
            name,
            version,
            hash,
            block.timestamp
        );
    }

    function getModel(uint256 id)
        public view returns (
            string memory name,
            string memory version,
            string memory hash,
            uint256 timestamp
        )
    {
        Model memory m = models[id];
        return (m.name, m.version, m.hash, m.timestamp);
    }
}