# SafeMoon Unit Test Example

## Folders
- `contract/`: compile contract
- `contract_storage/`: stored tested contracts
- `scritpt/`: test scripts wriiten by Dr. dan

## Install Brownie
Doc: https://eth-brownie.readthedocs.io/en/stable/index.html

## Configuration
Modify the file: brownie-cofiguration.yaml
- update networks
- update remappings
  - `brownie pm install OpenZeppelin/openzeppelin-contracts@4.0.0`
  - remapping @openzepplin to OpenZeppelin/openzeppelin-contracts@4.0.0
- update test_configuration to be the parameters of tested contract

## Test
- Compile the contract: `brownie compile`
- Run test case: `brownie test`
