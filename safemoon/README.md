# SafeMoon Unit Test Example

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
Run `brownie test`
