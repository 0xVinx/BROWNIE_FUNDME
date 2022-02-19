from brownie import accounts, network, exceptions
from scripts.helpful_scripts import get_account,LOCAL_BLOCKCHAIN_ENVIRONMENTS, deploy_mocks
import pytest
from scripts.fund_and_withdraw import fund,withdraw
from scripts.deploy import deploy_fund_me


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    enterance_fee = fund_me.getEnteranceFee() + 100
    tx = fund_me.fund({"from": account, "value": enterance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == enterance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)

def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    # fund_me.withdraw({"from": bad_actor})
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})

