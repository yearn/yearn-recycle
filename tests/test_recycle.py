def test_buy_underlying_and_recycle(recycle, interface, accounts, web3):
    uniswap = interface.UniswapV2Router02('0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D')
    weth = interface.ERC20('0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2')
    dai = interface.ERC20('0x6B175474E89094C44Da98b954EedeAC495271d0F')
    usdc = interface.ERC20('0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48')
    usdt = interface.USDT('0xdAC17F958D2ee523a2206206994597C13D831ec7')
    tusd = interface.ERC20('0x0000000000085d4780B73119b644AE5ecd22b376')
    yusd = interface.ERC20('0x5dbcF33D8c2E976c6b560249878e6F1491Bca25c')
    coins = [dai, usdc, usdt, tusd]

    # 1. buy some coins off uniswap
    deadline = web3.eth.getBlock('latest').timestamp + 600
    for coin in coins:
        uniswap.swapExactETHForTokens(0, [weth, coin], accounts[0], deadline, {'from': accounts[0], 'value': '1 ether'})
        assert coin.balanceOf(accounts[0]) > 0, 'coin not bought'
    
    # 2. grant approvals to the recycle contract
    for coin in coins:
        coin.approve(recycle, 2**256 - 1, {'from': accounts[0]})
        assert coin.allowance(accounts[0], recycle) == 2**256 - 1, 'approval not set'

    # 3. zap!
    tx = recycle.recycle({'from': accounts[0]})
    assert 'Recycled' in tx.events, 'not recycled'
    assert yusd.balanceOf(accounts[0]) == tx.events['Recycled']['received'], 'yusd balance mismatch'
