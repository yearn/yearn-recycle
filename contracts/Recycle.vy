# @version 0.2.4
from vyper.interfaces import ERC20

interface USDT:
    def transferFrom(_from: address, _to: address, _value: uint256): nonpayable
    def approve(_spender: address, _value: uint256): nonpayable

interface yCurveDeposit:
    def add_liquidity(uamounts: uint256[4], min_mint_amount: uint256): nonpayable

interface yVault:
    def deposit(amount: uint256): nonpayable

event Recycled:
    user: indexed(address)
    sent: uint256[4]
    received: uint256


safe: constant(address) = 0xFEB4acf3df3cDEA7399794D0869ef76A6EfAff52
ydeposit: constant(address) = 0xbBC81d23Ea2c3ec7e56D39296F0cbB648873a5d3
yvault: constant(address) = 0x5dbcF33D8c2E976c6b560249878e6F1491Bca25c
ycrv: constant(address) = 0xdF5e0e81Dff6FAF3A7e52BA697820c5e32D806A8
yusd: constant(address) = 0x5dbcF33D8c2E976c6b560249878e6F1491Bca25c

dai: constant(address) = 0x6B175474E89094C44Da98b954EedeAC495271d0F
usdc: constant(address) = 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48
usdt: constant(address) = 0xdAC17F958D2ee523a2206206994597C13D831ec7
tusd: constant(address) = 0x0000000000085d4780B73119b644AE5ecd22b376


@external
def recycle():
    dai_balance: uint256 = ERC20(dai).balanceOf(msg.sender)
    usdc_balance: uint256 = ERC20(usdc).balanceOf(msg.sender)
    usdt_balance: uint256 = ERC20(usdt).balanceOf(msg.sender)
    tusd_balance: uint256 = ERC20(tusd).balanceOf(msg.sender)

    if dai_balance > 0:
        ERC20(dai).transferFrom(msg.sender, self, dai_balance)
    if usdc_balance > 0:
        ERC20(usdc).transferFrom(msg.sender, self, usdc_balance)
    if usdt_balance > 0:
        USDT(usdt).transferFrom(msg.sender, self, usdt_balance)
    if tusd_balance > 0:
        ERC20(tusd).transferFrom(msg.sender, self, tusd_balance)
    
    if ERC20(dai).allowance(self, ydeposit) == 0:
        ERC20(dai).approve(ydeposit, MAX_UINT256)
        ERC20(usdc).approve(ydeposit, MAX_UINT256)
        USDT(usdt).approve(ydeposit, MAX_UINT256)
        ERC20(tusd).approve(ydeposit, MAX_UINT256)

    deposit_amounts: uint256[4] = [dai_balance, usdc_balance, usdt_balance, tusd_balance]
    yCurveDeposit(ydeposit).add_liquidity(deposit_amounts, 0)
    
    ycrv_balance: uint256 = ERC20(ycrv).balanceOf(self)
    if ERC20(ycrv).allowance(self, yvault) == 0:
        ERC20(ycrv).approve(yvault, MAX_UINT256)
    
    if ycrv_balance > 0:
        yVault(yvault).deposit(ycrv_balance)
    
    yusd_balance: uint256 = ERC20(yusd).balanceOf(self)
    ERC20(yusd).transfer(msg.sender, yusd_balance)

    assert ERC20(yusd).balanceOf(self) == 0, "leftover yusd balance"

    log Recycled(msg.sender, deposit_amounts, yusd_balance)
