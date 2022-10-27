pragma solidity 0.8.13;

// SPDX-License-Identifier: MIT

import "OpenZeppelin/openzeppelin-contracts@4.5.0/contracts/token/ERC20/IERC20.sol";
import "OpenZeppelin/openzeppelin-contracts@4.5.0/contracts/utils/Counters.sol";
import "OpenZeppelin/openzeppelin-contracts@4.5.0/contracts/token/ERC721/ERC721.sol";

import "./ZooNft.sol";

/// @notice contract to get tokens for open test of zoo dao battle arena.
contract ZooTokenFaucet is ERC721 {

	using Counters for Counters.Counter;
	Counters.Counter private _tokenIdTracker;                    // Token id tracker.

	IERC20 public zoo;
	IERC20 public dai;

	uint256 coef;

	uint256 public attemptLimit;
	uint256 public faucetAmount;                                 // Fixed amount of tokens to get.

	mapping (address => bool) whiteList;                         // WhiteList for admin functions.
	mapping (address => uint256) attemptAmount;

	address[] public collectionList;

	event tokensGiven(address indexed user);

	constructor (string memory name, string memory symbol, address _zoo, address _dai, address[] memory _collections) ERC721(name, symbol) 
	{
		zoo = IERC20(_zoo);
		dai = IERC20(_dai);

		collectionList = _collections;

		whiteList[msg.sender] = true;

		attemptLimit = 1;
		faucetAmount = 10000 * 10 ** 18;
	}

	/// @notice Function to get dai, zoo, and nft tokens for testnet.
	function getTokens() external 
	{
		require(attemptAmount[msg.sender] < attemptLimit, "reached attempt limit");
		uint256 zooBalance = zoo.balanceOf(address(this));
		uint256 daiBalance = zoo.balanceOf(address(this));
		require(zooBalance >= faucetAmount && daiBalance >= faucetAmount, "not enough tokens");

		zoo.transfer(msg.sender, faucetAmount);
		dai.transfer(msg.sender, faucetAmount);

		uint256 random = _computePseudoRandom() % 4;
		address collection = collectionList[random];

		ZooNft(collection).mint(msg.sender);
		ZooNft(collection).mint(msg.sender);

		attemptAmount[msg.sender] += 1;
		coef++;

		emit tokensGiven(msg.sender);
	}

	function _computePseudoRandom() internal view returns(uint256)
	{
		return uint256(keccak256(abi.encodePacked(blockhash(block.number - 1)))) + coef;
	}

	/// @notice Function for sending tokens for list of recipients.
	/// @param recipients - array of recipients.
	/// @param sendAmount - amount of zoo and dai tokens to send.
	function batchFaucet(address[] calldata recipients, uint256 sendAmount) external onlyWhiteList
	{
		uint256 totalTokensTransfered = sendAmount * recipients.length;
		uint256 zooBalance = zoo.balanceOf(address(this));
		uint256 daiBalance = zoo.balanceOf(address(this));
		require(zooBalance >= totalTokensTransfered && daiBalance >= totalTokensTransfered, "not enough tokens");

		for (uint256 i = 0; i < recipients.length; i++)
		{
			zoo.transfer(recipients[i], sendAmount);
			dai.transfer(recipients[i], sendAmount);
		}
	}

	/// @notice Function to mint test nft for msg.sender.
	function mint(address recipient) external onlyWhiteList
	{
		_tokenIdTracker.increment();
		uint256 newId = _tokenIdTracker.current();
		_mint(recipient, newId);
	}

	/// @notice Function to mint 30 nft for recipient.
	/// @notice admin only function.
	/// @param recipient - address receiver.
	function multiMint(address recipient) external onlyWhiteList
	{
		uint256 currentId = _tokenIdTracker.current();
		while (_tokenIdTracker.current() < currentId + 30)
		{
			_tokenIdTracker.increment();
			uint256 newId = _tokenIdTracker.current();
			_safeMint(recipient, newId);
		}
	}

	/// @notice Function to mint nfts for list of users.
	/// @notice admin only function.
	/// @param recipients - array of address to send nft.
	/// @param nftAmount - amount of nft to mint for every recipient.
	function batchMint(address[] calldata recipients, uint256 nftAmount) external onlyWhiteList
	{
		for (uint256 i = 0; i < recipients.length; i++) 
		{
			uint256 currentId = _tokenIdTracker.current();
			while (_tokenIdTracker.current() < currentId + nftAmount)
			{
				_tokenIdTracker.increment();
				uint256 newId = _tokenIdTracker.current();
				_safeMint(recipients[i], newId);
			}
		}
	}

	function returnTokens(uint256 zooAmount, uint256 daiAmount) external onlyWhiteList
	{
		zoo.transfer(msg.sender, zooAmount);
		dai.transfer(msg.sender, daiAmount);
	}

	function addToWhiteList(address user) external onlyWhiteList
	{
		whiteList[user] = true;
	}

	function batchAddToWhiteList(address[] calldata users) external onlyWhiteList
	{
		for (uint256 i = 0; i < users.length; i++) {
			whiteList[users[i]] = true;
		}
	}

	function changeAttemptLimit(uint256 amount) external onlyWhiteList
	{
		attemptLimit = amount;
	}

	function setFaucetAmount(uint256 amount) external onlyWhiteList
	{
		faucetAmount = amount;
	}

	modifier onlyWhiteList()
	{	
		require(whiteList[msg.sender] == true, "not whitelisted");
		_;
	}
}
