import pytest
from brownie import *


@pytest.fixture(scope='module')
def recycle(Recycle, accounts):
    return Recycle.deploy({'from': accounts[0]})
