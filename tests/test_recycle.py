import pytest


def buy_coins_on_uniswap(uniswap, coins, user):
    weth = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
    for coin in coins:
        uniswap.swapExactETHForTokens(0, [weth, coin], user, 10 ** 20, {'from': user, 'value': '1 ether'})
        assert coin.balanceOf(user) > 0, 'coin not bought'
        print('bought', coin.symbol(), coin.balanceOf(user) / 10 ** coin.decimals())


def set_allowances(coins, user, spender, unlimited=True):
    for coin in coins:
        allowance = 2 ** 256 - 1 if unlimited else 10 ** coin.decimals()
        coin.approve(spender, allowance, {'from': user})
        assert coin.allowance(user, spender) == allowance, 'invalid allowance'
        print('allowance', coin.symbol(), 'is set to', allowance)


@pytest.mark.parametrize('unlimited', [True, False])
def test_recycle(recycle, coins, uniswap, yusd, accounts, unlimited):
    buy_coins_on_uniswap(uniswap, coins, accounts[0])
    set_allowances(coins, accounts[0], recycle, unlimited)

    before = yusd.balanceOf(accounts[0])
    tx = recycle.recycle({'from': accounts[0]})
    assert yusd.balanceOf(accounts[0]) - before == tx.events['Recycled']['received_yusd']


def test_recycle_exact(recycle, coins, uniswap, yusd, accounts):
    buy_coins_on_uniswap(uniswap, coins, accounts[0])
    set_allowances(coins, accounts[0], recycle, True)

    before = yusd.balanceOf(accounts[0])
    balances = [coin.balanceOf(accounts[0]) for coin in coins]
    values = [10 ** coin.decimals() for coin in coins]
    tx = recycle.recycle_exact(*values, {'from': accounts[0]})
    assert yusd.balanceOf(accounts[0]) - before == tx.events['Recycled']['received_yusd']


@pytest.mark.parametrize('coin', range(5))
def test_recycle_single_coin(recycle, coins, uniswap, yusd, accounts, coin):
    buy_coins_on_uniswap(uniswap, [coins[coin]], accounts[0])
    set_allowances([coins[coin]], accounts[0], recycle, True)
    print(coins[coin].symbol(), coins[coin].balanceOf(accounts[0]))

    before = yusd.balanceOf(accounts[0])
    tx = recycle.recycle({'from': accounts[0]})
    assert yusd.balanceOf(accounts[0]) - before == tx.events['Recycled']['received_yusd']
