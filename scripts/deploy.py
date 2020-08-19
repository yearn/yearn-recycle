from brownie import Recycle, accounts


def main():
    deployer = accounts.load('banteg')
    return Recycle.deploy({'from': deployer})
