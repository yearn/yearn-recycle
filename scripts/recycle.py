import click
from brownie import Recycle, interface, accounts, history, rpc


def main():
    user = accounts[-1] if rpc.is_active() else accounts.load(input('brownie account: '))

    recycle = Recycle.at('0x5F07257145fDd889c6E318F99828E68A449A5c7A')

    dai = interface.ERC20('0x6B175474E89094C44Da98b954EedeAC495271d0F')
    usdc = interface.ERC20('0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48')
    usdt = interface.USDT('0xdAC17F958D2ee523a2206206994597C13D831ec7')
    tusd = interface.ERC20('0x0000000000085d4780B73119b644AE5ecd22b376')
    ycrv = interface.ERC20('0xdF5e0e81Dff6FAF3A7e52BA697820c5e32D806A8')
    yusd = interface.ERC20('0x5dbcF33D8c2E976c6b560249878e6F1491Bca25c')

    coins = [dai, usdc, usdt, tusd, ycrv]
    symbols = {ycrv: 'yCRV', yusd: 'yUSD'}

    balances = {symbols.get(coin, coin.symbol()): coin.balanceOf(user) / 10 ** coin.decimals() for coin in coins}
    balances = {name: balance for name, balance in balances.items() if balance > 0}

    print(f'Recycling...')
    for coin, balance in balances.items():
        print(f'  {coin} = {balance}')

    if not click.confirm('Continue?'):
        return

    for coin in coins:
        if coin.balanceOf(user) > coin.allowance(user, recycle):
            print(f'Approving {coin.name()}')
            coin.approve(recycle, 2 ** 256 - 1, {'from': user})

    tx = recycle.recycle({'from': user})
    print('Got', tx.events['Recycled']['received_yusd'] / 10 ** yusd.decimals(), 'yUSD')
