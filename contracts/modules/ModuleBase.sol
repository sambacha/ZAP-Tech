pragma solidity ^0.4.24;

import "../SecurityToken.sol";
import "../KYCRegistrar.sol";
import "../IssuingEntity.sol";

contract _ModuleBase {

	bytes32 public issuerID;
	IssuingEntity public issuer;

	constructor(address _issuer) public {
		issuer = IssuingEntity(_issuer);
		issuerID = issuer.issuerID();
	}

	modifier onlyIssuer () {
		require (uint8(issuer.issuerMap(msg.sender)) == 1);
		_;
	}

}

contract STModuleBase is _ModuleBase {

	SecurityToken public token;

	constructor(address _token, address _issuer) _ModuleBase(_issuer) public {
		token = SecurityToken(_token);
	}

	modifier onlyParent() {
		require (msg.sender == address(token) || msg.sender == address(token.issuer()));
		_;
	}

	function owner() public view returns (address) {
		return address(token);
	}

}

contract IssuerModuleBase is _ModuleBase {

	IssuingEntity public issuer;

	modifier onlyParent() {
		require (msg.sender == address(issuer));
		_;
	}

	function owner() public view returns (address) {
		return address(issuer);
	}

}
