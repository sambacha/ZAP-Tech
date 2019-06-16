#!/usr/bin/python3

import pytest

from brownie import accounts


@pytest.fixture(scope="module", autouse=True)
def setup(approve_many, issuer, nft):
    nft.mint(issuer, 100000, 0, "0x00", {'from': accounts[0]})
    issuer.setInvestorLimits((1, 0, 0, 0, 0, 0, 0, 0), {'from': accounts[0]})
    nft.transfer(accounts[1], 1000, {'from': accounts[0]})


@pytest.fixture(scope="module")
def setlimit(issuer):
    issuer.setInvestorLimits((0, 1, 0, 0, 0, 0, 0, 0), {'from': accounts[0]})


def test_total_investor_limit_blocked_issuer_investor(nft):
    '''total investor limit - blocked, issuer to investor'''
    with pytest.reverts("Total Investor Limit"):
        nft.transfer(accounts[2], 1000, {'from': accounts[0]})


def test_total_investor_limit_blocked_investor_investor(nft):
    '''total investor limit - blocked, investor to investor'''
    with pytest.reverts("Total Investor Limit"):
        nft.transfer(accounts[2], 500, {'from': accounts[1]})


def test_total_investor_limit_issuer_investor(nft):
    '''total investor limit - issuer to existing investor'''
    nft.transfer(accounts[1], 1000, {'from': accounts[0]})


def test_total_investor_limit_investor_investor(nft):
    '''total investor limit - investor to investor, full balance'''
    nft.transfer(accounts[2], 1000, {'from': accounts[1]})


def test_total_investor_limit_rating_blocked_issuer_investor(setlimit, nft):
    '''total investor limit, rating - blocked, issuer to investor'''
    with pytest.reverts("Total Investor Limit: Rating"):
        nft.transfer(accounts[3], 1000, {'from': accounts[0]})


def test_total_investor_limit_rating_blocked_investor_investor(setlimit, nft):
    '''total investor limit, rating - blocked, investor to investor'''
    with pytest.reverts("Total Investor Limit: Rating"):
        nft.transfer(accounts[3], 500, {'from': accounts[1]})


def test_total_investor_limit_rating_issuer_investor(setlimit, nft):
    '''total investor limit, rating - issuer to existing investor'''
    nft.transfer(accounts[1], 1000, {'from': accounts[0]})


def test_total_investor_limit_rating_investor_investor(setlimit, nft):
    '''total investor limit, rating - investor to investor, full balance'''
    nft.transfer(accounts[2], 1000, {'from': accounts[1]})


def test_total_investor_limit_rating_investor_investor_different_country(setlimit, nft):
    '''total investor limit, rating - investor to investor, different rating'''
    nft.transfer(accounts[2], 500, {'from': accounts[1]})