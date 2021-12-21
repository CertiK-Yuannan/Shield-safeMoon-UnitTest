import pytest
from brownie import accounts, interface
from brownie import Arker
import yaml

class ENV:
    with open('brownie-config.yaml') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    decimal = data['test_config']['parameter_contract']['decimal']
    transferAmt = 1 * data['test_config']['parameter_contract']['transferAmt'] * decimal
    maxReceivePercentage = data['test_config']['parameter_contract']['maxReceivePercentage_multiply_100'] / 100
    numTokensSellToAddToLiquidity = data['test_config']['parameter_contract']['numTokensSellToAddToLiquidity'] * decimal
    buyAmt_ETH = data['test_config']['parameter_contract']['buyAmt_ETH'] * 10**18

# Deployment
@pytest.fixture(scope="module")
def safemoon():
    safemoon = Arker.deploy({'from': accounts[0]})
    uniswapV2Router02 = interface.IUniswapV2Router02('0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D')

    # Add liquidity
    liquidityAmt = safemoon.totalSupply() / 10
    safemoon.approve(uniswapV2Router02.address, liquidityAmt, {'from': accounts[0]})
    uniswapV2Router02.addLiquidityETH(safemoon.address, liquidityAmt, 0, 0, accounts[0], 9999999999, {'from': accounts[0], 'amount': 50*1e18})

    return safemoon

# Test `swapAndLiquify` will not revert
def test_swapAndLiquify(safemoon):
    deployerBalanceBefore = safemoon.balanceOf(accounts[0])
    
    # transfer some token to safemoon contract 
    safemoon.transfer(safemoon.address, ENV.numTokensSellToAddToLiquidity, {'from': accounts[0]})
    
    # trigger swapAndLiqufy
    safemoon.transfer(accounts[1], ENV.transferAmt, {'from': accounts[0]})
    
    deployerBalanceAfter = safemoon.balanceOf(accounts[0])
    assert deployerBalanceBefore - deployerBalanceAfter == ( ENV.transferAmt + ENV.numTokensSellToAddToLiquidity )

# Test transfer is a deflation transfer
def test_transfer_deflation_singleAccount(safemoon):
    safemoon.transfer(accounts[1], ENV.transferAmt, {'from': accounts[0]})

    # Test single transaction received amount should no less that a threshold.
    assert safemoon.balanceOf(accounts[1]) >= ENV.maxReceivePercentage * ENV.transferAmt

    safemoon.transfer(accounts[2], safemoon.balanceOf(accounts[1]), {'from': accounts[1]})
        
    # Test whether there are tokens left after transferring
    assert safemoon.balanceOf(accounts[1]) == 0, "Account 1 balance not ZERO"

def test_transfer_deflation_totalSupplly(safemoon):
    safemoon.transfer(accounts[1], ENV.transferAmt, {'from': accounts[0]})
    totalSupplyBefore =  safemoon.balanceOf(accounts[1]) + safemoon.balanceOf(accounts[2]) + safemoon.balanceOf(accounts[3])

    for i in range(10):
        safemoon.transfer(accounts[2], safemoon.balanceOf(accounts[1]), {'from': accounts[1]})
        safemoon.transfer(accounts[3], safemoon.balanceOf(accounts[2]), {'from': accounts[2]})
        safemoon.transfer(accounts[1], safemoon.balanceOf(accounts[3]), {'from': accounts[3]})
    assert safemoon.balanceOf(accounts[1]) + safemoon.balanceOf(accounts[2]) + safemoon.balanceOf(accounts[3]) <= totalSupplyBefore, "Not deflation after transfer"


# Ensure safemoon can be bought from Uniswap
def test_buySafemoon_normal(safemoon):
    # Test buy SafeMoon normal situation
    uniswapV2Router02 = interface.IUniswapV2Router02('0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D')
    uniswapV2Router02.swapExactETHForTokensSupportingFeeOnTransferTokens(0, ['0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', safemoon.address], accounts[1], 9999999999, {'from': accounts[1], 'amount': ENV.buyAmt_ETH})
    assert safemoon.balanceOf(accounts[1]) > 0, "Normal case: SafeMoon tokens not recieve"

def test_buySafemoon_withSwapAndLiquify(safemoon):
    # Test buy SafeMoon trigger swap and liquidify situation
    # transfer some token to safemoon contract 
    safemoon.transfer(safemoon.address, ENV.numTokensSellToAddToLiquidity, {'from': accounts[0]})
    uniswapV2Router02 = interface.IUniswapV2Router02('0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D')
    uniswapV2Router02.swapExactETHForTokensSupportingFeeOnTransferTokens(0, ['0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', safemoon.address], accounts[1], 9999999999, {'from': accounts[1], 'amount': ENV.buyAmt_ETH})
    assert safemoon.balanceOf(accounts[1]) > 0, "Corner case: SafeMoon tokens not recieve"