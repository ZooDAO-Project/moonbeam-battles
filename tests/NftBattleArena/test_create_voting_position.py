import brownie
from brownie import chain


#
# Utility functions
#
# has _ before name because from is internal reserved word
def _from(account):
	return {"from": account}


def stake_nft(staking, account, nft, tokenId):
	nft.approve(staking.address, tokenId, _from(account))

	staking.stakeNft(nft.address, tokenId, _from(account))


def create_voting_position(voting, daiToken, account, stakingPositionId, daiAmount):
	daiToken.approve(voting, daiAmount, _from(account))

	return voting.createNewVotingPosition(stakingPositionId, daiAmount, _from(account))

# End of utility functions


def test_only_voting_can_call(accounts, tokens, battles):
	(vault, functions, governance, staking, voting, arena, listing, xZoo, jackpotA, jackpotB) = battles
	(zooToken, daiToken, linkToken, nft) = tokens

	stake_nft(staking, accounts[1], nft, 4)

	# Waiting for second stage
	chain.sleep(arena.firstStageDuration())

	staking_position_id = 1
	dai_amount = 10e18

	with brownie.reverts():
		arena.createVotingPosition(staking_position_id, accounts[0], dai_amount, _from(accounts[0]))

	tx = create_voting_position(voting, daiToken, accounts[2], staking_position_id, dai_amount)
	assert tx.status == 1


def test_creating_new_position(accounts, tokens, battles):
	(vault, functions, governance, staking, voting, arena, listing, xZoo, jackpotA, jackpotB) = battles
	(zooToken, daiToken, linkToken, nft) = tokens

	stake_nft(staking, accounts[1], nft, 4)

	# Waiting for second stage
	chain.sleep(arena.firstStageDuration())

	tx = create_voting_position(voting, daiToken, accounts[2], 1, 10e18)
	assert tx.status == 1


def test_dai_transfer(accounts, tokens, battles):
	(vault, functions, governance, staking, voting, arena, listing, xZoo, jackpotA, jackpotB) = battles
	(zooToken, daiToken, linkToken, nft) = tokens

	balance_before = daiToken.balanceOf(accounts[1], _from(accounts[1]))

	stake_nft(staking, accounts[1], nft, 4)

	vault_balance = daiToken.balanceOf(vault)

	# Waiting for second stage
	chain.sleep(arena.firstStageDuration())

	daiAmountToVote = 10e18
	create_voting_position(voting, daiToken, accounts[2], 1, daiAmountToVote)

	assert daiToken.balanceOf(accounts[2], _from(accounts[2])) == balance_before - daiAmountToVote
	assert daiToken.balanceOf(vault, _from(accounts[2])) == vault_balance + daiAmountToVote


def test_insufficient_funds(accounts, tokens, battles):
	(vault, functions, governance, staking, voting, arena, listing, xZoo, jackpotA, jackpotB) = battles
	(zooToken, daiToken, linkToken, nft) = tokens

	stake_nft(staking, accounts[1], nft, 4)

	# Waiting for second stage
	chain.sleep(arena.firstStageDuration())

	# More than account have
	daiAmountToVote = 5e25
	daiToken.approve(voting, daiAmountToVote, _from(accounts[1]))

	with brownie.reverts("Dai/insufficient-balance"):
		voting.createNewVotingPosition(1, daiAmountToVote, _from(accounts[1]))


def test_nft_mint(accounts, tokens, battles):
	(vault, functions, governance, staking, voting, arena, listing, xZoo, jackpotA, jackpotB) = battles
	(zooToken, daiToken, linkToken, nft) = tokens

	stake_nft(staking, accounts[1], nft, 4)

	# Waiting for second stage
	chain.sleep(arena.firstStageDuration())

	create_voting_position(voting, daiToken, accounts[2], 1, 10e18)

	assert voting.balanceOf(accounts[2], _from(accounts[2])) == 1
	assert voting.ownerOf(1, _from(accounts[2])) == accounts[2]


def test_non_existing_staking_id(accounts, tokens, battles):
	(vault, functions, governance, staking, voting, arena, listing, xZoo, jackpotA, jackpotB) = battles
	(zooToken, daiToken, linkToken, nft) = tokens

	# Waiting for second stage
	chain.sleep(arena.firstStageDuration())

	daiAmountToVote = 10e18
	daiToken.approve(voting, daiAmountToVote, _from(accounts[1]))

	with brownie.reverts("Not staked"):
		voting.createNewVotingPosition(123, daiAmountToVote, _from(accounts[1]))


def test_unstaked_nft(accounts, tokens, battles):
	(vault, functions, governance, staking, voting, arena, listing, xZoo, jackpotA, jackpotB) = battles
	(zooToken, daiToken, linkToken, nft) = tokens

	stake_nft(staking, accounts[1], nft, 4)

	staking.unstakeNft(1, _from(accounts[1]))

	# Waiting for second stage
	chain.sleep(arena.firstStageDuration())

	daiAmountToVote = 10e18
	daiToken.approve(voting, daiAmountToVote, _from(accounts[1]))

	with brownie.reverts("Not staked"):
		voting.createNewVotingPosition(1, daiAmountToVote, _from(accounts[1]))


def test_recording_new_voting_values(accounts, second_stage):
	(zooToken, daiToken, linkToken, nft) = second_stage[0]
	(vault, functions, governance, staking, voting, arena, listing, xZoo, jackpotA, jackpotB) = second_stage[1]

	daiAmountToVote = 20e18
	daiToken.approve(voting, daiAmountToVote, _from(accounts[1]))

	stakingPositionId = 1
	daiVoted = daiAmountToVote / 2
	voting.createNewVotingPosition(stakingPositionId, daiVoted, _from(accounts[1]))
	votingValues = arena.votingPositionsValues(1)

	assert votingValues["stakingPositionId"] == stakingPositionId
	#assert votingValues["startDate"] < chain.time() + 5 and votingValues["startDate"] > chain.time() - 5
	assert votingValues["daiInvested"] == daiVoted
	assert abs(arena.sharesToTokens.call(votingValues["yTokensNumber"]) - daiVoted) < 10
	assert votingValues["daiVotes"] == functions.computeVotesByDai(daiVoted)
	assert votingValues["votes"] == functions.computeVotesByDai(daiVoted)
	assert votingValues["startEpoch"] == arena.currentEpoch()
	assert votingValues["lastRewardedEpoch"] == arena.currentEpoch()


	stakingPositionId = 2
	voting.createNewVotingPosition(stakingPositionId, daiVoted, _from(accounts[1]))

	votingValues = arena.votingPositionsValues(2)

	assert votingValues["stakingPositionId"] == stakingPositionId
	#assert votingValues["startDate"] < chain.time() + 5 and votingValues["startDate"] > chain.time() - 5
	assert votingValues["daiInvested"] == daiVoted
	assert votingValues["yTokensNumber"] == arena.tokensToShares.call(daiVoted)
	assert votingValues["daiVotes"] == functions.computeVotesByDai(daiVoted)
	assert votingValues["votes"] == functions.computeVotesByDai(daiVoted)
	assert votingValues["startEpoch"] == arena.currentEpoch()
	assert votingValues["lastRewardedEpoch"] == arena.currentEpoch()


def test_recording_battle_reward(accounts, second_stage):
	(zooToken, daiToken, linkToken, nft) = second_stage[0]
	(vault, functions, governance, staking, voting, arena, listing, xZoo, jackpotA, jackpotB) = second_stage[1]

	daiAmountToVote = 20e18
	daiToken.approve(voting, daiAmountToVote, _from(accounts[1]))

	stakingPositionId = 1
	daiVoted = daiAmountToVote / 2
	voting.createNewVotingPosition(stakingPositionId, daiVoted, _from(accounts[1]))
	votingValues = arena.votingPositionsValues(1)

	epoch = arena.currentEpoch()
	reward = arena.rewardsForEpoch(stakingPositionId, epoch)

	assert abs(arena.sharesToTokens.call(reward["yTokens"]) - daiVoted) < 10
	assert reward["votes"] == functions.computeVotesByDai(daiVoted)

	stakingPositionId = 2
	voting.createNewVotingPosition(stakingPositionId, daiVoted, _from(accounts[1]))

	epoch = arena.currentEpoch()
	reward = arena.rewardsForEpoch(stakingPositionId, epoch)

	assert reward["yTokens"] == arena.tokensToShares.call(daiVoted)
	assert reward["votes"] == functions.computeVotesByDai(daiVoted)


def test_incrementing_number_of_nfts_with_non_zero_votes(accounts, second_stage):
	(zooToken, daiToken, linkToken, nft) = second_stage[0]
	(vault, functions, governance, staking, voting, arena, listing, xZoo, jackpotA, jackpotB) = second_stage[1]

	numberOfNftsWithNonZeroVotes = arena.numberOfNftsWithNonZeroVotes()

	daiAmountToVote = 20e18
	daiToken.approve(voting, daiAmountToVote, _from(accounts[1]))

	stakingPositionId = 1
	daiVoted = daiAmountToVote / 2
	voting.createNewVotingPosition(stakingPositionId, daiVoted, _from(accounts[1]))

	assert arena.numberOfNftsWithNonZeroVotes() == numberOfNftsWithNonZeroVotes + 1

	stakingPositionId = 2
	voting.createNewVotingPosition(stakingPositionId, daiVoted, _from(accounts[1]))

	assert arena.numberOfNftsWithNonZeroVotes() == numberOfNftsWithNonZeroVotes + 2


def test_emitting_event(accounts, second_stage):
	(zooToken, daiToken, linkToken, nft) = second_stage[0]
	(vault, functions, governance, staking, voting, arena, listing, xZoo, jackpotA, jackpotB) = second_stage[1]

	daiAmountToVote = 10e18
	daiToken.approve(voting, daiAmountToVote, _from(accounts[1]))

	stakingPositionId = 1
	tx = voting.createNewVotingPosition(stakingPositionId, daiAmountToVote, _from(accounts[1]))

	event = tx.events["CreatedVotingPosition"]
	assert event["currentEpoch"] == arena.currentEpoch()
	assert event["voter"] == accounts[1]
	assert event["stakingPositionId"] == stakingPositionId
	assert event["daiAmount"] == daiAmountToVote
	assert event["votes"] == daiAmountToVote * 1.3
	assert event["votingPositionId"] == 1
