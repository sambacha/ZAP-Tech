from brownie import *
from scripts.nftoken import main


def setup():
    config['test']['always_transact'] = False
    config['test']['default_contract_owner'] = True
    main()
    global token, issuer
    token = NFToken[0]
    issuer = IssuingEntity[0]

def add_tags_via_mint():
    '''Add tags through minting'''
    token.mint(a[1], 1000, 0, "0x01")
    token.mint(a[2], 1000, 0, "0x01")
    token.mint(a[3], 1000, 0, "0x01")
    token.mint(a[4], 1000, 0, "0x01")
    check.equal(token.getRange(1), (a[1],1,1001,0,"0x0001"))
    check.equal(token.getRange(1001), (a[2],1001,2001,0,"0x0001"))
    check.equal(token.getRange(2001), (a[3],2001,3001,0,"0x0001"))
    check.equal(token.getRange(3001), (a[4],3001,4001,0,"0x0001"))

def modify_range():
    '''Modify range'''
    token.mint(a[1], 1000, 0, "0x01")
    token.mint(a[2], 1000, 0, "0x01")
    token.mint(a[3], 1000, 0, "0x01")
    token.modifyRange(1001, 0, "0x1234")
    check.equal(token.getRange(1), (a[1], 1, 1001, 0, "0x0001"))
    check.equal(token.getRange(1001), (a[2], 1001, 2001, 0, "0x1234"))
    check.equal(token.getRange(2001), (a[3], 2001, 3001, 0, "0x0001"))

def modify_ranges():
    '''Modify ranges'''
    token.mint(a[1], 1000, 0, "0x01")
    token.mint(a[2], 1000, 0, "0x01")
    token.mint(a[3], 1000, 0, "0x01")
    token.modifyRanges(500, 2500, 0, "0x1234")
    check.equal(
        token.rangesOf(a[1]),
        ((1, 500), (500, 1001))
    )
    check.equal(
        token.rangesOf(a[2]),
        ((1001, 2001),)
    )
    check.equal(
        token.rangesOf(a[3]),
        ((2001, 2500), (2500, 3001))
    )

def modify_many():
    '''Modify many ranges'''
    token.mint(a[1], 1000, 0, "0x01")
    token.mint(a[2], 1000, 0, "0x01")
    token.mint(a[3], 1000, 0, "0x01")
    token.modifyRanges(500, 2500, 0, "0x1234")
    token.modifyRanges(700, 1500, 0, "0x1111")
    token.modifyRanges(1480, 2200, 0, "0x9999")
    check.equal(
        token.getRange(501),
        (a[1],500,700,0,"0x1234")
    )
    check.equal(
        token.getRange(701),
        (a[1],700,1001,0,"0x1111")
    )
    check.equal(
        token.getRange(1002),
        (a[2],1001,1480,0,"0x1111")
    )
    check.equal(
        token.getRange(1481),
        (a[2],1480,2001,0,"0x9999")
    )
    check.equal(
        token.getRange(2002),
        (a[3],2001,2200,0,"0x9999")
    )

def modify_join():
    '''Split and join ranges with modifyRange'''
    token.mint(a[1],10000, 0, "0x01")
    token.modifyRanges(2000, 4000, 0, "0x1234")
    check.equal(
        token.rangesOf(a[1]),
        ((1, 2000), (4000, 10001), (2000, 4000))
    )
    token.modifyRange(2000, 0, "0x01")
    check.equal(
        token.rangesOf(a[1]),
        ((1, 10001),)
    )

def modify_join_many():
    '''Split and join with modifyRanges'''
    token.mint(a[1],10000, 0, "0x01")
    token.modifyRanges(2000, 4000, 0, "0x1234")
    token.modifyRanges(1000, 6000, 0, "0x01")
    check.equal(
        token.rangesOf(a[1]),
        ((1, 10001),)
    )

def time():
    '''Block transfers with time lock'''
    token.mint(a[1], 10000, rpc.time()+20, "0x00")
    check.reverts(
        token.transfer,
        (a[2], 1000, {'from':a[1]})
    )
    rpc.sleep(21)
    token.transfer(a[2],1000,{'from':a[1]})


def time_partial():
    '''Partially block a transfer with time'''
    token.mint(a[1], 10000, 0, "0x00")
    token.modifyRanges(2001,6001, rpc.time()+20, "0x00")
    check.true(token.getRange(2001)['_stop'] == 6001)
    token.transfer(a[2], 4000, {'from': a[1]})
    check.equal(
        token.rangesOf(a[1]),
        ((8001,10001), (2001, 6001))
    )
    rpc.sleep(25)
    token.transfer(a[2], 6000, {'from':a[1]})
    check.equal(
        token.rangesOf(a[2]),
        ((1,10001),)
    )