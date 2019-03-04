pragma solidity >=0.4.24 <0.5.0;

/**
	Common interface for all modules - these are the minimum required methods
	that must be included to attach the contract
*/
interface IBaseModule {
	function getPermissions()
		external
		pure
		returns
	(
		bytes4[] permissions,
		bytes4[] hooks,
		bool[] hooksActive,
		bool[] hooksAlways
	);
	function getOwner() external view returns (address);
	function name() external view returns (string);
}

/** SecurityToken module interface */
interface ISTModule {
	
	function token() external returns (address);
	
	/* 0x70aaf928 */
	function checkTransfer(
		address[2] _addr,
		bytes32 _authID,
		bytes32[2] _id,
		uint8[2] _rating,
		uint16[2] _country,
		uint256 _value
	)
		external
		view
		returns (bool);

	/* 0x35a341da */
	function transferTokens(
		address[2] _addr,
		bytes32[2] _id,
		uint8[2] _rating,
		uint16[2] _country,
		uint256 _value
	)
		external
		returns (bool);

	/* 0x8745b31c */
	function transferTokensCustodian(
		address _custodian,
		address[2] _addr,
		bytes32[2] _id,
		uint8[2] _rating,
		uint16[2] _country,
		uint256 _value
	)
		external
		returns (bool);

	/* 0xb1a1a455 */
	function modifyAuthorizedSupply(
		address _token,
		uint256 _oldSupply,
		uint256 _newSupply
	)
		external
		returns (bool);

	/* 0x741b5078 */
	function totalSupplyChanged(
		address _addr,
		bytes32 _id,
		uint8 _rating,
		uint16 _country,
		uint256 _old,
		uint256 _new
	)
		external
		returns (bool);
}

/** NFToken module interface */
interface INFTModule {

	function token() external returns (address);

	/* 0x70aaf928 */
	function checkTransfer(
		address[2] _addr,
		bytes32 _authID,
		bytes32[2] _id,
		uint8[2] _rating,
		uint16[2] _country,
		uint256 _value
	)
		external
		view
		returns (bool);

	/* 5a5a8ad8 */
	function checkTransferRange(
		bytes32 _authID,
		bytes32[2] _id,
		address[2] _addr,
		uint8[2] _rating,
		uint16[2] _country,
		uint48[2] _range
	)
		external
		view
		returns (bool);

	/* 0x979c114f */
	function transferTokenRange(
		bytes32[2] _id,
		address[2] _addr,
		uint8[2] _rating,
		uint16[2] _country,
		uint48[2] _range
	)
		external
		returns (bool);

	/* 0xb1a1a455 */
	function modifyAuthorizedSupply(
		address _token,
		uint256 _oldSupply,
		uint256 _newSupply
	)
		external
		returns (bool);

	/* 0x741b5078 */
	function totalSupplyChanged(
		address _addr,
		bytes32 _id,
		uint8 _rating,
		uint16 _country,
		uint256 _old,
		uint256 _new
	)
		external
		returns (bool);
}

/** IssuingEntity module interface */
interface IIssuerModule {

	/* 0x9a5150fc */
	function checkTransfer(
		address _token,
		bytes32 _authID,
		bytes32[2] _id,
		uint8[2] _rating,
		uint16[2] _country
	)
		external
		view
		returns (bool);

	/* 0xb446f3ca */
	function tokenTotalSupplyChanged(
		address _token,
		bytes32 _id,
		uint8 _rating,
		uint16 _country,
		uint256 _old,
		uint256 _new
	)
		external
		returns (bool);
}

/** Custodian module interface */
interface ICustodianModule {

	/**
		@notice Custodian sent tokens
		@dev
			Called after a successful token transfer from the custodian.
			Use 0x31b45d35 as the hook value for this method.
		@param _token Token address
		@param _id Recipient ID
		@param _value Amount of tokens transfered
		@param _stillOwner Is recipient still a beneficial owner for this token?
		@return bool success
	 */
	function sentTokens(
		address _token,
		bytes32 _id,
		uint256 _value,
		bool _stillOwner
	)
		external
		returns (bool);

	/**
		@notice Custodian received tokens
		@dev
			Called after a successful token transfer to the custodian.
			Use 0xa0e7f751 as the hook value for this method.
		@param _token Token address
		@param _id Recipient ID
		@param _value Amount of tokens transfered
		@return bool success
	 */
	function receivedTokens(
		address _token,
		bytes32 _id,
		uint256 _value
	)
		external
		returns (bool);

	/* 0x7054b724 */
	function internalTransfer(
		address _token,
		bytes32 _fromID,
		bytes32 _toID,
		uint256 _value,
		bool _stillOwner
	)
		external
		returns (bool);

	/* 0x054d1c76 */
	function ownershipReleased(
		address _issuer,
		bytes32 _id
	)
		external
		returns (bool);
}