# Yearn Recycle

A contract that recycles all your [DAI, USDC, USDT, TUSD, yCRV] into yCRV and further into yUSD vault.

## Usage

You need to grant allowances on up to five tokens to this contract before using it. This needs to be done for all non-zero amount and it only needs to be done once.

### Using Brownie

Use the Brownie script to automatically set all approvals and recycle all your coins into yUSD.

```python
$ brownie accounts import user keystore.json
$ brownie run recycle --network mainnet
```

### Using Etherscan

1. Call `approve(0x5F07257145fDd889c6E318F99828E68A449A5c7A, 115792089237316195423570985008687907853269984665640564039457584007913129639935)` for all non-zero balances:
- [DAI](https://etherscan.io/address/0x6B175474E89094C44Da98b954EedeAC495271d0F#writeContract)
- [USDC](https://etherscan.io/address/0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48#writeProxyContract)
- [USDT](https://etherscan.io/address/0xdAC17F958D2ee523a2206206994597C13D831ec7#writeContract)
- [TUSD](https://etherscan.io/address/0x0000000000085d4780B73119b644AE5ecd22b376#writeProxyContract)
- [yCRV](https://etherscan.io/address/0xdF5e0e81Dff6FAF3A7e52BA697820c5e32D806A8#writeContract)

2. Call `recycle()` [here](https://etherscan.io/address/0x5F07257145fDd889c6E318F99828E68A449A5c7A#writeContract).

## Deployments

### v0.2.0
`0x5F07257145fDd889c6E318F99828E68A449A5c7A`

- Add support for yCRV deposits
- Add a Brownie script to set the needed approvals and recycle
- Honor allowances in `recycle()`, deposit `min(balance, allowance)`
- Add an ability to recycle custom amounts with `recycle_exact(dai, usdc, usdt, tusd, ycrv)`

Reviewed by:
- @iamdefinitelyahuman

### v0.1.0
`0x78e307F6e8584DaA0D85aDD918c0e3e4dD469A9C`

Initial release, features `recycle()` function which converts [DAI, USDC, USDT, TUSD] to yUSD.

Reviewed by:
- @samczsun
- @andrecronje
- @vshvsh

## Frontends

TBD

### Integration caveats

Check for `token.balanceOf(user)` and `token.allowance(user, recycle)` for each of DAI, USDC, USDT, TUSD, yCRV

For tokens with non-zero balances and `balance > allowance`, call `token.approve(recycle, MAX_UINT256)`

At this point you can call `recycle.recycle()`

You can get the exact amounts in and out from the transaction receipt event called `Recycled(user, sent_dai, sent_usdc, sent_usdt, sent_tusd, sent_ycrv, received_yusd)`

You can also allow depositing partial amounts (sliders?) or skipping some of the coins (checkboxes?). For this you need to calculate the exact amounts and pass them into `recycle.recycle_exact(dai, usdc, usdt, tusd, ycrv)`

Note that USDT is not ERC20-compliant, it doesn't return bool for `approve` and also requires first resetting the `allowance` to zero before changing it to another value.
