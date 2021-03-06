# TODO: Add tests here that show the normal operation of this strategy
#       Suggestions to include:
#           - strategy loading and unloading (via Vault addStrategy/revokeStrategy)
#           - change in loading (from low to high and high to low)
#           - strategy operation at different loading levels (anticipated and "extreme")
from brownie import Wei, reverts
from useful_methods import genericStateOfVault, genericStateOfStrat
import brownie

def test_operation(web3, chain, vault, strategy, token, amount, dai, dai_vault, whale, gov, guardian, strategist):

    # whale approve weth vault to use weth
    token.approve(vault, 2 ** 256 - 1, {"from": whale})

    print('cdp id: {}'.format(strategy.cdpId()))
    print(f'type of strategy: {type(strategy)} @ {strategy}')
    print(f'type of weth vault: {type(vault)} @ {vault}')
    print()

    # start deposit
    vault.deposit(amount, {"from": whale})
    print(f'whale deposit done with {amount/1e18} weth\n')


    print("\n****** Initial Status ******")
    print("\n****** yfi ******")
    genericStateOfStrat(strategy, token, vault)
    genericStateOfVault(vault, token)
    print("\n****** Dai ******")
    genericStateOfVault(dai_vault, dai)


    print("\n****** Harvest yfi ******")
    strategy.harvest({'from': strategist})

    print("\n****** yfi ******")
    genericStateOfStrat(strategy, token, vault)
    genericStateOfVault(vault, token)
    print("\n****** Dai ******")
    genericStateOfVault(dai_vault, dai)

    # withdraw yfi
    print('\n****** withdraw yfi ******')
    print(f'whale\'s yfi vault share: {vault.balanceOf(whale)/1e18}')
    vault.withdraw(Wei('1 ether'), {"from": whale})
    print(f'withdraw 1 ether done')
    print(f'whale\'s yfi vault share: {vault.balanceOf(whale)/1e18}')

    # transfer dai to strategy due to rounding issue
    dai.transfer(strategy, Wei('1 wei'), {"from": gov})

    # withdraw all yfi
    print('\n****** withdraw all yfi ******')
    print(f'whale\'s yfi vault share: {vault.balanceOf(whale)/1e18}')
    vault.withdraw({"from": whale})
    print(f'withdraw all yfi')
    print(f'whale\'s yfi vault share: {vault.balanceOf(whale)/1e18}')

    # try call tend
    print('\ncall tend')
    strategy.tend()
    print('tend done')
