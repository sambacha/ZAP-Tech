#!/usr/bin/python3

import functools
import pytest

from brownie import accounts, compile_source

module_source = """
pragma solidity 0.4.25;

contract TestModule {{

    address owner;
    bool hookReturn = true;

    constructor(address _owner) public {{ owner = _owner; }}
    function getOwner() external view returns (address) {{ return owner; }}

    function getPermissions()
        external
        pure
        returns
    (
        bytes4[] permissions,
        bytes4[] hooks,
        uint256 hookBools
    )
    {{
        bytes4[] memory _hooks = new bytes4[](1);
        _hooks[0] = {};
        return (permissions, _hooks, uint256(0)-1);
    }}

    function setReturn(bool _return) external {{
        hookReturn = _return;
    }}

    function {}) external returns (bool) {{
        if (!hookReturn) {{
            revert();
        }}
        return true;
    }}

}}"""


@pytest.fixture(scope="module", autouse=True)
def testhook(approve_many, org, token):
    token.mint(org, 100000, {'from': accounts[0]})
    hook = functools.partial(_hook, org, token)
    yield hook


def test_checkTransfer(testhook, token):
    source = '''checkTransfer(
        address[2] _addr,
        bytes32 _authID,
        bytes32[2] _id,
        uint8[2] _rating,
        uint16[2] _country,
        uint256 _value'''
    testhook(token.checkTransfer, (accounts[0], accounts[1], 1000), source, "0x70aaf928")


def test_transferTokens(testhook, token):
    source = '''transferTokens(
        address[2] _addr,
        bytes32[2] _id,
        uint8[2] _rating,
        uint16[2] _country,
        uint256 _value'''
    testhook(token.transfer, (accounts[1], 1000), source, "0x35a341da")


def test_transferTokensCustodian(testhook, token, cust):
    source = '''transferTokensCustodian(
        address _custodian,
        address[2] _addr,
        bytes32[2] _id,
        uint8[2] _rating,
        uint16[2] _country,
        uint256 _value'''
    token.transfer(accounts[2], 10000, {'from': accounts[0]})
    token.transfer(cust, 5000, {'from': accounts[2]})
    testhook(cust.transferInternal, (token, accounts[2], accounts[3], 100), source, "0x8b5f1240")


def test_totalSupplyChanged(testhook, org, token, cust):
    source = '''totalSupplyChanged(
        address _addr,
        bytes32 _id,
        uint8 _rating,
        uint16 _country,
        uint256 _old,
        uint256 _new'''
    testhook(token.burn, (org, 1000), source, "0x741b5078")
    testhook(token.mint, (accounts[2], 1000), source, "0x741b5078")


def _hook(org, token, fn, args, source, sig):
    args = list(args) + [{'from': accounts[0]}]
    source = module_source.format(sig, source)
    project = compile_source(source)
    module = project.TestModule.deploy(token, {'from': accounts[0]})
    fn(*args)
    org.attachModule(token, module, {'from': accounts[0]})
    fn(*args)
    module.setReturn(False, {'from': accounts[0]})
    with pytest.reverts():
        fn(*args)
    org.detachModule(token, module, {'from': accounts[0]})
    fn(*args)