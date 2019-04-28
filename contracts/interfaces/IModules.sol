pragma solidity >=0.4.24 <0.5.0;

/**
	@notice Common interface for all modules
	@dev
		these are the minimum required methods that MUST be included to
		attach the module to the parent contract
*/
interface IBaseModule {
	function getPermissions()
		external
		pure
		returns
	(
		bytes4[] permissions,
		bytes4[] hooks,
		uint256 hookBools
	);
	function getOwner() external view returns (address);
	function name() external view returns (string);
}

/**
	@notice SecurityToken module interface
	@dev These are all the possible hook point methods for token modules
*/
contract ISTModule is IBaseModule {
	
	function token() external returns (address);
	
	/**
		@notice Check if a transfer is possible
		@dev
			Called before a token transfer to check if it is permitted
			Hook signature: 0x70aaf928
		@param _addr sender and receiver addresses
		@param _authID id hash of caller
		@param _id sender and receiver id hashes
		@param _rating sender and receiver investor ratings
		@param _country sender and receiver country codes
		@param _value amount of tokens to be transfered
		@return bool success
	 */
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

	/**
		@notice Token transfer
		@dev
			Called a token transfer has completed
			Hook signature: 0x35a341da
		@param _addr sender and receiver addresses
		@param _id sender and receiver id hashes
		@param _rating sender and receiver investor ratings
		@param _country sender and receiver country codes
		@param _value amount of tokens to be transfered
		@return bool success
	 */
	function transferTokens(
		address[2] _addr,
		bytes32[2] _id,
		uint8[2] _rating,
		uint16[2] _country,
		uint256 _value
	)
		external
		returns (bool);

	/**
		@notice Token custodial internal transfer
		@dev
			Called a custodian internal token transfer has completed
			Hook signature: 0x8b5f1240
		@param _custodian custodian address
		@param _addr sender and receiver addresses
		@param _id sender and receiver id hashes
		@param _rating sender and receiver investor ratings
		@param _country sender and receiver country codes
		@param _value amount of tokens to be transfered
		@return bool success
	 */
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


	/**
		@notice Modify authorized supply
		@dev
			Called before modifying the authorized supply of a token
			Hook signature: 0xa5f502c1
		@param _token
	 */
	function modifyAuthorizedSupply(
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

/**
	@notice NFToken module interface
	@dev
		These are all the possible hook point methods for NFToken modules
		All SecurityToken module hook points are also available
*/
contract INFTModule is ISTModule {

	/* 0x2d79c6d7 taggable */
	function checkTransferRange(
		address[2] _addr,
		bytes32 _authID,
		bytes32[2] _id,
		uint8[2] _rating,
		uint16[2] _country,
		uint48[2] _range
	)
		external
		view
		returns (bool);

	/* 0xead529f5 taggable */
	function transferTokenRange(
		address[2] _addr,
		bytes32[2] _id,
		uint8[2] _rating,
		uint16[2] _country,
		uint48[2] _range
	)
		external
		returns (bool);

}

/**
	@notice IssuingEntity module interface
	@dev These are all the possible hook point methods for issuer modules
*/
contract IIssuerModule is IBaseModule {

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

/**
	@notice Custodian module interface
	@dev These are all the possible hook point methods for custodian modules
*/
contract ICustodianModule is IBaseModule {

	/**
		@notice Custodian sent tokens
		@dev
			Called after a successful token transfer from the custodian.
			Hook signature: 0xb4684410
		@param _token Token address
		@param _to Recipient address
		@param _value Amount of tokens transfered
		@return bool success
	 */
	function sentTokens(
		address _token,
		address _to,
		uint256 _value
	)
		external
		returns (bool);

	/**
		@notice Custodian received tokens
		@dev
			Called after a successful token transfer to the custodian.
			Hook signature: 0xb15bcbc4
		@param _token Token address
		@param _from Sender address
		@param _value Amount of tokens transfered
		@return bool success
	 */
	function receivedTokens(
		address _token,
		address _from,
		uint256 _value
	)
		external
		returns (bool);

	/**
		@notice Custodian internal token transfer
		@dev
			Called after a successful internal token transfer by the custodian
			Hook signature: 0x44a29e2a
		@param _token Token address
		@param _from Sender address
		@param _value Amount of tokens transfered
		@return bool success
	 */
	function internalTransfer(
		address _token,
		address _from,
		address _to,
		uint256 _value
	)
		external
		returns (bool);
}