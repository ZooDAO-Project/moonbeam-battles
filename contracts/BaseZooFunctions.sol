pragma solidity 0.8.13;

// SPDX-License-Identifier: MIT

import "./interfaces/IZooFunctions.sol";
import "./NftBattleArena.sol";
import "OpenZeppelin/openzeppelin-contracts@4.5.0/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

/// @title Contract BaseZooFunctions.
/// @notice Contracts for base implementation of some ZooDao functions.
contract BaseZooFunctions is Ownable, VRFConsumerBase
{
	NftBattleArena public battles;

	constructor (address _vrfCoordinator, address _link, uint256 firstStage, uint256 secondStage, uint256 thirdStage, uint256 fourthstage, uint256 fifthstage) VRFConsumerBase(_vrfCoordinator, _link) 
	{
		chainLinkFee = 0.1 * 10 ** 18;
		keyHash = 0x6c3699283bda56ad74f6b855546325b68d482e983852a7a82979cc4807b641f4;

		firstStageDuration = firstStage;      // Duration of first stage(stake).
		secondStageDuration = secondStage;    // Duration of second stage(DAI).
		thirdStageDuration = thirdStage;      // Duration of third stage(Pair).
		fourthStageDuration = fourthstage;    // Duration fourth stage(ZOO).
		fifthStageDuration = fifthstage;      // Duration of fifth stage(Winner).
	}

	mapping (uint256 => uint256) public randomNumberByEpoch;

	uint256 internal chainLinkFee;
	bytes32 internal keyHash;

	bool public isRandomFulfilled;
	bool public isRandomRequested;
	uint256 internal randomResult;  // Random number for battles.

	uint256 public firstStageDuration;      // Duration of first stage(stake).
	uint256 public secondStageDuration;     // Duration of second stage(DAI).
	uint256 public thirdStageDuration;      // Duration of third stage(Pair).
	uint256 public fourthStageDuration;     // Duration fourth stage(ZOO).
	uint256 public fifthStageDuration;      // Duration of fifth stage(Winner).
	
	/// @notice Function for setting address of _nftBattleArena contract.
	/// @param _nftBattleArena - address of _nftBattleArena contract.
	/// @param owner - address of contract owner, should be aragon dao.
	function init(address payable _nftBattleArena, address owner) external onlyOwner {
		battles = NftBattleArena(_nftBattleArena);

		transferOwnership(owner);                       // transfer ownership to dao.
	}

	/// @notice Function to reset random number from battles.
	function resetRandom() external onlyArena
	{
		randomResult = 0;
		isRandomRequested = false;
		isRandomFulfilled = false;
	}

	function getStageDurations() external view returns (uint256, uint256, uint256, uint256, uint256, uint256 epochDuration)
	{
		epochDuration = firstStageDuration + secondStageDuration + thirdStageDuration + fourthStageDuration + fifthStageDuration;
		return (firstStageDuration, secondStageDuration, thirdStageDuration, fourthStageDuration, fifthStageDuration, epochDuration);
	}

	function fulfillRandomness(bytes32 requestId, uint256 randomness) internal override 
	{
		randomResult = randomness;                      // Random number from chainlink.
		isRandomFulfilled = true;
	}

	/// @notice Function to request random from chainlink or blockhash.
	function requestRandomNumber() external onlyArena
	{
		require(!isRandomRequested, "Random is already requested");
		require(battles.getCurrentStage() == Stage.FifthStage, "Random wasn't reset");

		randomResult = _computePseudoRandom();
		randomNumberByEpoch[battles.currentEpoch()] = randomResult;
		isRandomFulfilled = true;
		isRandomRequested = true;
	}

	function computePseudoRandom() external view returns (uint256)
	{
		return _computePseudoRandom();
	}

	function _computePseudoRandom() internal view returns(uint256)
	{
		return uint256(keccak256(abi.encodePacked(blockhash(block.number - 1))));
	}

	function getRandomResultByEpoch(uint256 epoch) external view returns (uint256)
	{
		return randomNumberByEpoch[epoch];
	}

	function getRandomResult() external view returns(uint256) {
		require(isRandomRequested, "Random wasn't requested");
		require(isRandomFulfilled, "Random wasn't fulfilled yet");

		return randomResult;
	}

	/// @notice Function for choosing winner in battle.
	/// @param votesForA - amount of votes for 1st candidate.
	/// @param votesForB - amount of votes for 2nd candidate.
	/// @param random - generated random number.
	/// @return bool - returns true if 1st candidate wins.
	function decideWins(uint256 votesForA, uint256 votesForB, uint256 random) external pure returns (bool)
	{
		uint256 mod = random % (votesForA + votesForB);
		return mod < votesForA;
	}

	/// @notice Function for calculating voting with Dai in vote battles.
	/// @param amount - amount of dai used for vote.
	/// @return votes - final amount of votes after calculating.
	function computeVotesByDai(uint256 amount) external view returns (uint256 votes)
	{
		if (block.timestamp < battles.epochStartDate() + battles.firstStageDuration() + battles.secondStageDuration() / 3)
		{
			votes = amount * 13 / 10;                                          // 1.3 multiplier for votes.
		}
		else if (block.timestamp < battles.epochStartDate() + battles.firstStageDuration() + ((battles.secondStageDuration() * 2) / 3))
		{
			votes = amount;                                                    // 1.0 multiplier for votes.
		}
		else
		{
			votes = amount * 7 / 10;                                           // 0.7 multiplier for votes.
		}
	}

	/// @notice Function for calculating voting with Zoo in vote battles.
	/// @param amount - amount of Zoo used for vote.
	/// @return votes - final amount of votes after calculating.
	function computeVotesByZoo(uint256 amount) external view returns (uint256 votes)
	{
		if (block.timestamp < battles.epochStartDate() + battles.firstStageDuration() + battles.secondStageDuration() + battles.thirdStageDuration() + (battles.fourthStageDuration() / 3))
		{
			votes = amount * 13 / 10;                                         // 1.3 multiplier for votes.
		}
		else if (block.timestamp < battles.epochStartDate() + battles.firstStageDuration() + battles.secondStageDuration() + battles.thirdStageDuration() + (battles.fourthStageDuration() * 2) / 3)
		{
			votes = amount;                                                   // 1.0 multiplier for votes.
		}
		else
		{
			votes = amount * 7 / 10;                                          // 0.7 multiplier for votes.
		}
	}

	function setStageDuration(Stage stage, uint256 duration) external onlyOwner {
		// require(duration >= 2 days && 10 days >= duration, "incorrect duration");

		if (stage == Stage.FirstStage) {
			firstStageDuration = duration;
		}
		else if (stage == Stage.SecondStage)
		{
			secondStageDuration = duration;
		}
		else if (stage == Stage.ThirdStage)
		{
			thirdStageDuration = duration;
		}
		else if (stage == Stage.FourthStage)
		{
			fourthStageDuration = duration;
		}
		else if (stage == Stage.FifthStage)
		{
			fifthStageDuration = duration;
		}
	}

	modifier onlyArena() {
		require(msg.sender == address(battles), 'Only arena contract can make call');
		_;
	}
}
