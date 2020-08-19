# Yearn Recycle

A contract that recycles all your [DAI, USDC, USDT, TUSD] into yCRV and further into yUSD vault.

## Usage

You need to grant allowances on four tokens to this contract before using it. This only needs to be done once.

### Using Brownie

```python
$ brownie accounts import user keystore.json

$ brownie console --network mainnet

user = accounts.load('user')

recycle = Recycle.at('0x78e307F6e8584DaA0D85aDD918c0e3e4dD469A9C')

dai = interface.ERC20('0x6B175474E89094C44Da98b954EedeAC495271d0F')
usdc = interface.ERC20('0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48')
usdt = interface.USDT('0xdAC17F958D2ee523a2206206994597C13D831ec7')
tusd = interface.ERC20('0x0000000000085d4780B73119b644AE5ecd22b376')

for coin in [dai, usdc, usdt, tusd]:
    coin.approve(recycle, 2**256 - 1, {'from': user})

recycle.recycle({'from': user})
```

### Using Etherscan

1. Call `approve(0x78e307F6e8584DaA0D85aDD918c0e3e4dD469A9C, 115792089237316195423570985008687907853269984665640564039457584007913129639935)` for [DAI](https://etherscan.io/address/0x6B175474E89094C44Da98b954EedeAC495271d0F#writeContract), [USDC](https://etherscan.io/address/0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48#writeProxyContract), [USDT](https://etherscan.io/address/0xdAC17F958D2ee523a2206206994597C13D831ec7#writeContract), [TUSD](https://etherscan.io/address/0x0000000000085d4780B73119b644AE5ecd22b376#writeProxyContract).
2. Call `recycle()` [here](https://etherscan.io/address/0x78e307F6e8584DaA0D85aDD918c0e3e4dD469A9C#writeContract).

## Deployments

Ethereum Mainnet: `0x78e307F6e8584DaA0D85aDD918c0e3e4dD469A9C`

## Audits

TBD.
