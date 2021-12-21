from brownie import accounts, network, interface, config, Contract
# from brownie import SafeMoon
from brownie import DefectiveContract
from brownie._config import CONFIG
from brownie.network.web3 import web3
from brownie.network.state import Chain
import random

# simulate the attack https://etherscan.io/tx/0xcd7dae143a4c0223349c16237ce4cd7696b1638d116a72755231ede872ab70fc
# without the flashloan part



def main():
    num = 10
    # Environment Setup
    network.disconnect('mainnet-fork')
    # CONFIG.networks['mainnet-fork']['cmd_settings']['fork'] = 'https://mainnet.infura.io/v3/cf64e9aa7e5047a8afd17394a21ac158@12955062'
    CONFIG.networks['mainnet-fork']['cmd_settings']['fork'] = 'https://eth-mainnet.alchemyapi.io/v2/8sIinwGOjt4xg880x4o8T0YyNEctOPkT@12955062'


    CONFIG.networks['mainnet-fork']['explorer'] = 'https://api.etherscan.io/api'
    network.connect('mainnet-fork')
    # print(web3.eth.blockNumber)
    # print(network.show_active())
    # print(CONFIG.networks['mainnet-fork'])

    # UniswapV2Router02 = interface.IUniswapV2Router02('0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D')
    # print("test")
    # WETH = interface.IERC20('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2')
    # print('the balance is: ' + str(WETH.totalSupply()))

    # Deployment
    # safemoon = SafeMoon.deploy({'from': accounts[0]})
    safemoon = DefectiveContract.deploy({'from': accounts[0]})
    # print(safemoon.totalSupply())

    initialSetup(safemoon)
    # test1(safemoon)
    # test2(safemoon)
    # # test3(safemoon)
    # test4(safemoon)

    # functionList = [test1,test2,test4]
    #functionList = [simulateTransfer, simulateBuy, simulateSell]
    # random.choice(functionList)(safemoon)
    #randomChooseMultiFunctions(functionList,safemoon,num)

    # chain = Chain()

def randomChooseMultiFunctions(functionList, deployment, num):
    for _ in range(num):
        random.choice(functionList)(deployment)  

def initialSetup(safemoon):
    # Add liquidity
    print('Initializing...')
    uniswapV2Router02 = interface.IUniswapV2Router02('0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D')
    safemoon.approve(uniswapV2Router02.address, 1e12, {'from': accounts[0]})
    uniswapV2Router02.addLiquidityETH(safemoon.address, 1e12, 0, 0, accounts[0], 9999999999, {'from': accounts[0], 'amount': 1e18})

    # Set initial balances
    safemoon.transfer(accounts[1], 1e13, {'from': accounts[0]})
    safemoon.transfer(accounts[2], 1e13, {'from': accounts[0]})
    safemoon.transfer(accounts[3], 1e13, {'from': accounts[0]})
    print('Finished initialization.')

# total supply should be less than total supply before
def test1(safemoon):
    print("check total supply should be less than total supply before")
    tokensToSend = 2000
    tokensToReceive = tokensToSend * 90 / 100
    account1 = accounts[1]
    account2 = accounts[2]
    account3 = accounts[3]
    balance1Before = safemoon.balanceOf(account1)
    balance2Before = safemoon.balanceOf(account2)
    balance3Before = safemoon.balanceOf(account3)
    totalSupplyBefore = balance1Before + balance2Before + balance3Before
    safemoon.approve(account2, tokensToSend, {'from': accounts[1]})
    safemoon.transfer(account2, tokensToSend, {'from': accounts[1]})
    balance1After= safemoon.balanceOf(account1)
    balance2After = safemoon.balanceOf(account2)
    balance3After = safemoon.balanceOf(account3)
    totalSupplyAfter = balance1After + balance2After + balance3After
    diff1 = balance1After + tokensToSend - balance1Before
    diff2 = balance2After - tokensToReceive - balance2Before
    # diff3 = balance3After - balance3Before
    # print(balance1After,balance2After,balance3After)
    # ratio1 = balance1After / diff1
    # ratio2 = balance2After / diff2
    # ratio3 = balance3After / diff3
    # print(ratio1,ratio2)
    # assert(ratio3 == ratio2)
    assert(totalSupplyAfter < totalSupplyBefore)



# should transfer tokens correctly while one of accounts is excluded
def test2(safemoon):
    print("check should transfer tokens correctly while one of accounts is excluded")
    tokensToSend = 2000
    tokensToReceive = tokensToSend * 90 / 100
    account1 = accounts[1]
    account2 = accounts[2]
    account3 = accounts[3]
    safemoon.excludeFromReward(account1, {'from': accounts[0]})
    balance1Before = safemoon.balanceOf(account1)
    balance2Before = safemoon.balanceOf(account2)
    balance3Before = safemoon.balanceOf(account3)
    totalSupplyBefore = balance1Before + balance2Before + balance3Before
    safemoon.approve(account2, tokensToSend, {'from': accounts[1]})
    safemoon.transfer(account2, tokensToSend, {'from': accounts[1]})
    balance1After= safemoon.balanceOf(account1)
    balance2After = safemoon.balanceOf(account2)
    balance3After = safemoon.balanceOf(account3)
    totalSupplyAfter = balance1After + balance2After + balance3After
    diff1 = balance1After + tokensToSend - balance1Before
    diff2 = balance2After - tokensToReceive - balance2Before
    # diff3 = balance3After - balance3Before
    # print(balance1After,balance2After,balance3After)
    # ratio1 = balance1After / diff1
    # ratio2 = balance2After / diff2
    # ratio3 = balance3After / diff3
    # print(ratio1,ratio2)
    # assert(ratio3 == ratio2)
    assert(totalSupplyAfter < totalSupplyBefore)



# should stop burning tokens as soon as the total amount reaches 1% of the initial
# Note: only when the safemoon fork has burn() function/interface
def test3(safemoon):
    account1 = accounts[1]
    account2 = accounts[2]
    account3 = accounts[3]
    safemoon.burn(1000000, {'from': accounts[1]})
    safemoon.burn(100000000, {'from': accounts[3]})
    balanceBeforeBurn = safemoon.balanceOf(account2)
    assert(balanceBefore == 2200000)

    safemoon.burn(balanceBeforeBurn-2100000, {'from': accounts[2]})
    balanceAfterBurn = safemoon.balanceOf(account2)
    totalSupplyBeforeSend = safemoon.totalSupply()
    safemoon.transfer(account1, 1000, {'from': account2})
    totalSupplyAfterSend = safemoon.totalSupply()
    assert(totalSupplyAfterSend == totalSupplyBeforeSend)

    balance1 = safemoon.balanceOf(account1)
    balance2 = safemoon.balanceOf(account2)
    assert(balanceAfterBurn == (balance1+balance2+1))


# 'Exclude / Include address'
def test4(safemoon):
    print("check exclude / include address")
    account4 = accounts[4]
    safemoon.excludeFromReward(account4)
    assert(safemoon.isExcludedFromReward(account4) == True), "test1"

    safemoon.includeInReward(account4)
    assert(safemoon.isExcludedFromReward(account4) == False), "test2"

    safemoon.excludeFromFee(account4)
    assert(safemoon.isExcludedFromFee(account4) == True), "test3"

    safemoon.includeInFee(account4)
    assert(safemoon.isExcludedFromFee(account4) == False), "test4"

# Simulate a transfer with random sender, recipient and amount.
def simulateTransfer(safemoon):
    print("Simulate transfer")

    iAccountList = range(4)
    iSender = random.choice(iAccountList)
    iRecipient = random.choice([i for i in iAccountList if i != iSender])
    sender = accounts[iSender]
    recipient = accounts[iRecipient]

    print("account {} balance: {}".format(iSender, sender.balance()))

    balanceOfSender = safemoon.balanceOf(sender)
    if balanceOfSender == 0:
        return
    amount = random.randint(1, balanceOfSender)

    safemoon.transfer(recipient, amount, {'from': sender})
    print("{} sent {} to {}".format(sender, amount, recipient))

# Simulate a buy with random buyer and amount using Uniswap.
def simulateBuy(safemoon):
    print("Simulate buy")
    wethAddress = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'
    uniswapV2Router02 = interface.IUniswapV2Router02('0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D')

    buyer = accounts[random.choice(range(1, 4))]
    balanceOfBuyer = buyer.balance()
    if balanceOfBuyer == 0:
        return
    amount = random.randint(1, int(balanceOfBuyer/100))

    print('{} is buying the token with {} wei.'. format(buyer, amount))
    uniswapV2Router02.swapExactETHForTokens(0, [wethAddress, safemoon.address], buyer, 9999999999, {'from': buyer, 'amount': amount})

# Simulate a sell with random seller and amount using Uniswap.
def simulateSell(safemoon):
    print("Simulate sell")
    wethAddress = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'
    uniswapV2Router02 = interface.IUniswapV2Router02('0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D')

    seller = accounts[random.choice(range(1, 4))]
    balanceOfSeller = safemoon.balanceOf(seller)
    if balanceOfSeller == 0:
        return
    amount = random.randint(1, min(int(balanceOfSeller/100), safemoon._maxTxAmount()))

    print('{} is selling {} token for WETH.'. format(seller, amount))
    safemoon.approve(uniswapV2Router02.address, amount, {'from': seller})
    uniswapV2Router02.swapExactTokensForETHSupportingFeeOnTransferTokens(amount, 0, [safemoon.address, wethAddress], seller, 9999999999, {'from': seller})
