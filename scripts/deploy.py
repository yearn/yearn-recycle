from brownie import Recycle, accounts


def main():
    deployer = accounts.load(input('brownie account: '))
    return Recycle.deploy({'from': deployer})
