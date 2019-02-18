#!/usr/bin/python3

from brownie import *

def setup():
    global a, countries
    countries = [1,2,3]
    a = accounts
    global owner1, owner2
    global authority1, authority2
    global investor1, investor2
    global scratch1 
    owner1 = a[0]; 
    owner2 = a[1]
    authority1 = a[2]; 
    authority2 = a[3]
    investor1 = a[4]; 
    investor2 = a[5]
    scratch1 = a[9]


################################################
# Tests for management of Addresses / ID mappings

# Owners controlling owners

def owner_can_add_a_new_owner_address():
    registrar = owner1.deploy(KYCRegistrar, [owner1, owner2], 1)
    ownerID = registrar.getID(owner1)
    txr = registrar.registerAddresses(ownerID, [scratch1])
    check.equal(txr.return_value, True)
    check.equal(registrar.getID(scratch1), ownerID) # new address gets added to existing ID
    check.event_fired(txr, 'RegisteredAddresses' , 1)

    
def one_owner_cant_add_a_new_owner_address_when_multisig():
    registrar = owner1.deploy(KYCRegistrar, [owner1, owner2], 2)
    ownerID = registrar.getID(owner1)
    txr = registrar.registerAddresses(ownerID, [scratch1])
    check.equal(txr.return_value, False)

def owner_cant_restrict_an_owner_address_multisig():
    registrar = owner1.deploy(KYCRegistrar, [owner1, owner2], 2)
    ownerID = registrar.getID(owner1)
    txr = registrar.restrictAddresses(ownerID, [owner2])
    check.equal(txr.return_value, False)
    check.event_not_fired(txr, 'RestrictedAddresses')

def owner_can_restrict_an_owner_address():
    registrar = owner1.deploy(KYCRegistrar, [owner1, owner2], 1)
    ownerID = registrar.getID(owner1)
    txr = registrar.restrictAddresses(ownerID, [owner2])
    check.equal(txr.return_value, True)
    check.event_fired(txr, 'RestrictedAddresses' , 1)

def owner_can_unrestrict_an_owner_address():
    registrar = owner1.deploy(KYCRegistrar, [owner1, owner2], 1)
    ownerID = registrar.getID(owner1)
    txr = registrar.restrictAddresses(ownerID, [owner2], {'from':owner1})
    check.equal(txr.return_value, True)
    check.event_fired(txr, 'RestrictedAddresses' , 1)
    txr = registrar.registerAddresses(ownerID, [owner2], {'from':owner1})
    check.equal(txr.return_value, True)
    check.event_fired(txr, 'RegisteredAddresses' , 1)

def owner_cant_unrestrict_their_own_address():
    registrar = owner1.deploy(KYCRegistrar, [owner1, owner2], 1)
    ownerID = registrar.getID(owner1)
    txr = registrar.restrictAddresses(ownerID, [owner2])
    check.reverts(registrar.registerAddresses, (ownerID, [owner2], {'from':owner2}))

def restricted_owner_address_cant_add_a_new_owner_address():
    registrar = owner1.deploy(KYCRegistrar, [owner1, owner2], 1)
    ownerID = registrar.getID(owner1)
    txr = registrar.restrictAddresses(ownerID, [owner2])
    check.reverts(registrar.registerAddresses, (ownerID, [scratch1], {'from':owner2}))

# Owners controlling authorities

def owner_can_add_a_new_authority_address_multisig():
    registrar = owner1.deploy(KYCRegistrar, [owner1, owner2], 2)
    registrar.addAuthority([authority1], countries, 1, {'from':owner1})
    check.equal(registrar.getID(authority1), 0)
    registrar.addAuthority([authority1], countries, 1, {'from':owner2})
    check.not_equal(registrar.getID(authority1), 0)

def owner_can_restrict_an_authority_address():
    registrar = owner1.deploy(KYCRegistrar, [owner1, owner2], 1)
    registrar.addAuthority([authority1, authority2], countries, 1, {'from':owner1})
    authorityID = registrar.getID(authority1)
    txr = registrar.restrictAddresses(authorityID, [authority1], {'from':owner1})
    check.equal(txr.return_value, True)
    check.event_fired(txr, 'RestrictedAddresses' , 1)

def owner_cant_restrict_too_many_authority_addresses():
    # "When restricing addresses associated to an authority, you cannot reduce the number
    #  of addresses such that the total remaining is lower than the multi-sig threshold
    #  value for that authority." 
    registrar = owner1.deploy(KYCRegistrar, [owner1, owner2], 1)
    registrar.addAuthority([authority1, authority2, scratch1], countries, 2, {'from':owner1})
    authorityID = registrar.getID(authority1)
    txr = registrar.restrictAddresses(authorityID, [authority1], {'from':owner1})
    check.equal(txr.return_value, True)
    check.event_fired(txr, 'RestrictedAddresses' , 1)
    check.reverts(registrar.restrictAddresses, (authorityID, [authority1], {'from':owner1}))


# Authorities

def authority_can_add_a_new_investor_address_in_their_country():
    # given two authorities for country X then both can add addresses
    # for an investor in that country - even if not the original authority
    registrar = owner1.deploy(KYCRegistrar, [owner1, owner2], 1)
    registrar.addAuthority([authority1], countries, 1, {'from':owner1})
    registrar.addAuthority([authority2], countries, 1, {'from':owner1})
    id_ = '0x9c93effa8c8bc959961e24dbda7cbc1be362a1df'
    registrar.addInvestor(id_, 1, 1, 1, 4550275220, [investor1], {'from':authority1})
    id_ = registrar.getID(investor1)
    registrar.registerAddresses(id_, [investor2], {'from':authority2})
    id2 = registrar.getID(investor2)
    check.equal(id_, id2)

# Investors

def investor_cant_add_a_new_address():
    # only owner/authorities can do this
    registrar = owner1.deploy(KYCRegistrar, [owner1, owner2], 1)
    registrar.addAuthority([authority1], countries, 1, {'from':owner1})
    id_ = '0x9c93effa8c8bc959961e24dbda7cbc1be362a1df'
    registrar.addInvestor(id_, 1, 1, 1, 4550275220, [investor1], {'from':authority1})
    id_ = registrar.getID(investor1)
    check.reverts(registrar.registerAddresses, (id_, [investor2], {'from':investor1}))
