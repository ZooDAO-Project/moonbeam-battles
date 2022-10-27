pragma solidity 0.8.13;

// SPDX-License-Identifier: MIT

import "OpenZeppelin/openzeppelin-contracts@4.5.0/contracts/token/ERC721/ERC721.sol";
import "OpenZeppelin/openzeppelin-contracts@4.5.0/contracts/token/ERC20/IERC20.sol";
import "OpenZeppelin/openzeppelin-contracts@4.5.0/contracts/access/Ownable.sol";
import "./NftBattleArena.sol";

/// @title NftVotingPosition
/// @notice contract for voters to interacte with BattleArena functions
contract NftVotingPosition is ERC721, Ownable
{
	event NftBattleArenaSet(address nftBattleArena);

	NftBattleArena public nftBattleArena;
	IERC20 public dai;
	IERC20 public zoo;

	constructor(string memory _name, string memory _symbol, address _dai, address _zoo) ERC721(_name, _symbol)
	{
		dai = IERC20(_dai);
		zoo = IERC20(_zoo);

	}

	modifier onlyVotingOwner(uint256 votingPositionId) {
		require(ownerOf(votingPositionId) == msg.sender, "Not the owner of voting");
		_;
	}

	function setNftBattleArena(address _nftBattleArena) external onlyOwner
	{
		require(address(nftBattleArena) == address(0));

		nftBattleArena = NftBattleArena(_nftBattleArena);

		emit NftBattleArenaSet(_nftBattleArena);
	}

	function createNewVotingPosition(uint256 stakingPositionId, uint256 amount) external
	{
		require(amount != 0, "zero vote not allowed");                                        // Requires for vote amount to be more than zero.
		dai.transferFrom(msg.sender, address(nftBattleArena), amount);                        // Transfers DAI to arena contract for vote.
		(,uint256 votingPositionId) = nftBattleArena.createVotingPosition(stakingPositionId, msg.sender, amount);
		_safeMint(msg.sender, votingPositionId);
	}

	function addDaiToPosition(uint256 votingPositionId, uint256 amount) external onlyVotingOwner(votingPositionId) returns (uint256 votes)
	{
		dai.transferFrom(msg.sender, address(nftBattleArena), amount);                        // Transfers DAI to arena contract for vote.
		nftBattleArena.addDaiToVoting(votingPositionId, msg.sender, amount, 0);               // zero for yTokens coz its not swap.
	}

	function addZooToPosition(uint256 votingPositionId, uint256 amount) external onlyVotingOwner(votingPositionId) returns (uint256 votes) 
	{
		zoo.transferFrom(msg.sender, address(nftBattleArena), amount);                        // Transfers ZOO to arena contract for vote.
		nftBattleArena.addZooToVoting(votingPositionId, msg.sender, amount);
	}

	function withdrawDaiFromVotingPosition(uint256 votingPositionId, address beneficiary, uint256 daiNumber) external onlyVotingOwner(votingPositionId)
	{
		nftBattleArena.withdrawDaiFromVoting(votingPositionId, msg.sender, beneficiary, daiNumber, false);
	}

	function withdrawZooFromVotingPosition(uint256 votingPositionId, uint256 zooNumber, address beneficiary) external onlyVotingOwner(votingPositionId)
	{
		nftBattleArena.withdrawZooFromVoting(votingPositionId, msg.sender, zooNumber, beneficiary);
	}

	function claimRewardFromVoting(uint256 votingPositionId, address beneficiary) external onlyVotingOwner(votingPositionId) returns (uint256)
	{
		return nftBattleArena.claimRewardFromVoting(votingPositionId, msg.sender, beneficiary);
	}

	/// @notice Function to move votes from one position to another.
	/// @notice If moving to nft not voted before(i.e. creating new position), then newVotingPosition should be zero.
	/// @param votingPositionId - Id of position votes moving from.
	/// @param daiNumber - amount of dai moving.
	/// @param newStakingPositionId - id of stakingPosition moving to.
	/// @param newVotingPosition - id of voting position moving to, if exist. If there are no such, should be zero.
	function swapVotesFromPosition(uint256 votingPositionId, uint256 daiNumber, uint256 newStakingPositionId, address beneficiary, uint256 newVotingPosition) external onlyVotingOwner(votingPositionId)
	{
		require(daiNumber != 0, "zero vote not allowed");                                        // Requires for vote amount to be more than zero.
		require(newVotingPosition == 0 || ownerOf(newVotingPosition) == msg.sender, "Not the owner of voting");

		uint256 newVotingPosition1 = nftBattleArena.swapPositionVotes(votingPositionId, msg.sender, beneficiary, daiNumber, newStakingPositionId, newVotingPosition);

		if (newVotingPosition == 0)
		{
			_safeMint(msg.sender, newVotingPosition1);
		}
	}

	/// Claims rewards from multiple voting positions
	/// @param votingPositionIds array of voting positions indexes
	/// @param beneficiary address to transfer reward to
	function batchClaimRewardsFromVotings(uint256[] calldata votingPositionIds, address beneficiary) external returns (uint256 reward)
	{
		for (uint256 i = 0; i < votingPositionIds.length; i++)
		{
			require(msg.sender == ownerOf(votingPositionIds[i]), "Not the owner of voting");

			reward += nftBattleArena.claimRewardFromVoting(votingPositionIds[i], msg.sender, beneficiary);
		}
	}

	function batchWithdrawDaiFromVoting(uint256[] calldata votingPositionIds, address beneficiary, uint256 daiNumber) external
	{
		for (uint256 i = 0; i < votingPositionIds.length; i++)
		{
			require(msg.sender == ownerOf(votingPositionIds[i]), "Not the owner of voting");

			nftBattleArena.withdrawDaiFromVoting(votingPositionIds[i], msg.sender, beneficiary, daiNumber, false);
		}
	}

	function batchWithdrawZooFromVoting(uint256[] calldata votingPositionIds, uint256 zooNumber, address beneficiary) external
	{
		for (uint256 i = 0; i < votingPositionIds.length; i++)
		{
			require(msg.sender == ownerOf(votingPositionIds[i]), "Not the owner of voting");

			nftBattleArena.withdrawZooFromVoting(votingPositionIds[i], msg.sender, zooNumber, beneficiary);
		}
	}

	/// @notice Function to claim incentive reward for voting, proportionally of collection weight in ve-Model pool.
	function claimIncentiveVoterReward(uint256 votingPositionId, address beneficiary) external returns (uint256)
	{
		require(ownerOf(votingPositionId) == msg.sender, "Not the owner!");             // Requires to be owner of position.

		uint256 reward = nftBattleArena.calculateIncentiveRewardForVoter(votingPositionId);

		zoo.transfer(beneficiary, reward);

		return reward;
	}

	function batchClaimIncentiveVoterReward(uint256[] calldata votingPositionIds, address beneficiary) external returns (uint256 reward)
	{
		for (uint256 i = 0; i < votingPositionIds.length; i++)
		{
			require(ownerOf(votingPositionIds[i]) == msg.sender, "Not the owner!");             // Requires to be owner of position.

			reward += nftBattleArena.calculateIncentiveRewardForVoter(votingPositionIds[i]);
		}
		zoo.transfer(beneficiary, reward);
	}
}