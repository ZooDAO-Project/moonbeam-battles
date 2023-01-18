pragma solidity 0.8.13;

// SPDX-License-Identifier: MIT

import "OpenZeppelin/openzeppelin-contracts@4.5.0/contracts/token/ERC721/IERC721.sol";
import "OpenZeppelin/openzeppelin-contracts@4.5.0/contracts/token/ERC721/ERC721.sol";
import "OpenZeppelin/openzeppelin-contracts@4.5.0/contracts/token/ERC20/IERC20.sol";
import "./interfaces/IVault.sol";
import "./NftBattleArena.sol";
import "./lib/IterableMapping.sol";
import "./interfaces/IZooFunctions.sol";

/// @title JackPot
/// @notice contract for jackpot reward from arena.
contract Jackpot is ERC721
{
	using IterableMapping for IterableMapping.Map;

	IterableMapping.Map internal map;

	uint256 public positionIndex = 1;

	VaultAPI public vault;

	IERC721 public positionContract;

	NftBattleArena public arena;

	IZooFunctions public zooFunctions;

	// epoch => id of position
	mapping (uint256 => uint256) public winners;

	// epoch => positionId => claimed?
	mapping (uint256 => mapping(uint256 => bool)) public claimedBy;

	mapping (address => uint256) public tokenOfOwner;

	mapping (uint256 => uint256) public stakedPositionsById;

	event Staked(uint256 positionId, address staker, address beneficiary, uint256 jackpotPositionId);

	event Unstaked(uint256 jackpotPositionId, address owner, address beneficiary, uint256 zooPositionId);

	event Claimed(uint256 indexed id, uint256 epoch, address owner, address beneficiary, uint256 rewards);

	event WinnerChosen(uint256 epoch, uint256 indexed winner);

	event NftBattleArenaSet(address nftBattleArena);

	constructor (address _positionContract, address _vault, address _functions, string memory _name, string memory _symbol) ERC721(_name, _symbol)
	{
		vault = VaultAPI(_vault);
		positionContract = IERC721(_positionContract);
		zooFunctions = IZooFunctions(_functions);
	}

	function setNftBattleArena(address payable _nftBattleArena) external
	{
		require(address(arena) == address(0));

		arena = NftBattleArena(_nftBattleArena);

		emit NftBattleArenaSet(_nftBattleArena);
	}

	/// @notice Function to choose jackpot winner in selected epoch.
	function chooseWinner(uint256 epoch) external
	{
		require(epoch < arena.currentEpoch(), "only played epochs");
		require(winners[epoch] == 0, "winner has been chosen");
		uint256 random = zooFunctions.getRandomResultByEpoch(epoch);
		require(random != 0, "requestRandom has not been called");
		winners[epoch] = map.get(map.getKeyAtIndex(random % map.size()));

		emit WinnerChosen(epoch, winners[epoch]);
	}

	/// @notice Function to stake Nft position to take part in jackpot.
	function stake(uint256 id, address beneficiary) external returns (uint256)
	{
		require(tokenOfOwner[msg.sender] == 0, "Caller must have only one jackpot position");

		positionContract.transferFrom(msg.sender, address(this), id);
		_mint(beneficiary, positionIndex);
		stakedPositionsById[positionIndex] = id;
		map.set(positionIndex, positionIndex);
		tokenOfOwner[msg.sender] = positionIndex;

		emit Staked(id, msg.sender, beneficiary, positionIndex);
		return positionIndex++;
	}

	/// @notice Function to unstake Nft position.
	function unstake(uint256 id, address beneficiary) external
	{
		require(ownerOf(id) == msg.sender);
		uint256 zooPositionId = stakedPositionsById[id];
		require(zooPositionId != 0);
		stakedPositionsById[id] = 0;
		map.remove(id);
		tokenOfOwner[msg.sender] = 0;

		positionContract.transferFrom(address(this), beneficiary, zooPositionId);
		emit Unstaked(id, msg.sender, beneficiary, zooPositionId);
	}

	/// @notice Function to check if selected position have reward or not in selected epoch. 
	function checkReward(uint256 id, uint256 epoch) public view returns (uint256 yvTokensReward)
	{
		if (winners[epoch] == id && !claimedBy[epoch][id])
		{
			return arena.jackpotRewardsAtEpoch(epoch);
		}
		else
			return 0;
	}

	/// @notice Function to claim reward from jackpot.
	function claimReward(uint256 id, uint256 epoch, address beneficiary) external returns (uint256 rewards)
	{
		require(ownerOf(id) == msg.sender);

		uint256 redeemAmount = checkReward(id, epoch);
		claimedBy[epoch][id] = true;
		vault.redeem(redeemAmount);
		rewards = IERC20(arena.dai()).balanceOf(address(this));
		IERC20(arena.dai()).transfer(beneficiary, rewards);

		emit Claimed(id, epoch, msg.sender, beneficiary, rewards);
	}
}