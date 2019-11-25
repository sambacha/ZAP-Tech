#!/usr/bin/python3

import pytest

from brownie import accounts


@pytest.fixture(scope="module", autouse=True)
def setup(org):
    for i in range(6):
        accounts.add()
        accounts[0].transfer(accounts[-1], "1 ether")
    org.addAuthority(accounts[-6:-3], [], 2000000000, 1, {'from': accounts[0]})


@pytest.fixture(scope="module")
def cust(OwnedCustodian):
    yield accounts[0].deploy(OwnedCustodian, [accounts[0]], 1)


@pytest.fixture(scope="module")
def token2(SecurityToken, org):
    yield accounts[0].deploy(SecurityToken, org, "Test Token2", "TS2", 1000000)


def test_setCountry(multisig, org):
    multisig(org.setCountry, 1, True, 1, [0] * 8)


def test_setCountries(multisig, org):
    multisig(org.setCountries, [1, 2], [1, 1], [0, 0])


def test_setInvestorLimits(multisig, org):
    multisig(org.setInvestorLimits, [0] * 8)


def test_setDocumentHash(multisig, org):
    multisig(org.setDocumentHash, "blah blah", "0x1234")


def test_setVerifier(multisig, org):
    multisig(org.setVerifier, accounts[9], False)


def test_addCustodian(multisig, org, cust):
    multisig(org.addCustodian, cust)


def test_addToken(multisig, org, token2):
    multisig(org.addToken, token2)


def test_setEntityRestriction(multisig, org):
    multisig(org.setEntityRestriction, "0x11", True)


def test_setTokenRestriction(multisig, org, token):
    multisig(org.setTokenRestriction, token, False)


def test_setGlobalRestriction(multisig, org):
    multisig(org.setGlobalRestriction, True)