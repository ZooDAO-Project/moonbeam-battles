import brownie
from brownie import chain, ZERO_ADDRESS

def calculate_incentive_reward_for_staker(account, veZoo, arena, staking, stakingPositionId):
	stakingPosition = arena.stakingPositionsValues(stakingPositionId)
	collection = stakingPosition["collection"]

	#arena.updateInfo(stakingPositionId)
	arena.updateInfoAboutStakedNumber(collection)
	veZoo.updateCurrentEpochAndReturnPoolWeight(collection)
	veZoo.updateCurrentEpochAndReturnPoolWeight(ZERO_ADDRESS)

	end = arena.currentEpoch() if stakingPosition["endEpoch"] == 0 else stakingPosition["endEpoch"]
	reward = 0
	start = stakingPosition["lastEpochOfIncentiveReward"]

	for i in range(start, end):
		startEpoch = veZoo.getEpochNumber(arena.epochsStarts(i))
		endEpoch = veZoo.getEpochNumber(arena.epochsStarts(i + 1))
		total_votes = arena.rewardsForEpoch(stakingPositionId, i)["votes"]
		dai_votes = stakingPosition

		for j in range(startEpoch, endEpoch):
			if veZoo.poolWeight(ZERO_ADDRESS, j) != 0:
				reward += arena.baseStakerReward() * veZoo.poolWeight(collection, j) // veZoo.poolWeight(ZERO_ADDRESS, j) // arena.numberOfStakedNftsInCollection(i, collection)

	return reward


def test_one_collection_incentive_reward_of_staker(accounts, finished_epoch):
	(zooToken, daiToken, linkToken, nft) = finished_epoch[0]
	(vault, functions, governance, staking, voting, arena, listing, xZoo, jackpotA, jackpotB) = finished_epoch[1]

	arena.updateInfoAboutStakedNumber(nft)
	assert arena.numberOfStakedNftsInCollection(1, nft) > 0
	assert arena.numberOfStakedNftsInCollection(2, nft) > 0
	
	result = calculate_incentive_reward_for_staker(accounts[0], listing, arena, staking, 1)

	tx = staking.claimIncentiveStakerReward(1, accounts[-1], {"from": accounts[0]})

	

	assert tx.return_value == result
	assert zooToken.balanceOf(accounts[-1]) == result