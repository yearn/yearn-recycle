# Yearn Recycle

A contract that recycles all your [DAI, USDC, USDT, TUSD] into yCRV and further into yUSD vault.

## Usage

You need to grant allowances on four tokens to this contract before using it.

```
ERC20(dai).approve(recycle, MAX_UINT256)
ERC20(usdc).approve(recycle, MAX_UINT256)
USDT(usdt).approve(recycle, MAX_UINT256)
ERC20(tusd).approve(recycle, MAX_UINT256)
```

Then you can simply call it to receive yUSD back.

```
recycle.recycle()
```

## Deployments

Ethereum Mainnet: `0x78e307F6e8584DaA0D85aDD918c0e3e4dD469A9C`

## Audits

TBD.
