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


def test_owner_requirement(accounts, battles, tokens):
	(vault, functions, governance, staking, voting, arena, listing, xZoo, jackpotA, jackpotB) = battles
	(zooToken, daiToken, linkToken, nft) = tokens


	stake_nft(staking, accounts[1], nft, 4)

	chain.sleep(arena.firstStageDuration())

	create_voting_position(voting, daiToken, accounts[2], 1, 10e18)

	additionalDai = 10e18

	# TODO: add error msg
	with brownie.reverts():
		voting.addDaiToPosition(1, additionalDai, _from(accounts[1]))


def test_dai_transfer(accounts, tokens, battles):
	(vault, functions, governance, staking, voting, arena, listing, xZoo, jackpotA, jackpotB) = battles
	(zooToken, daiToken, linkToken, nft) = tokens

	balance_before = daiToken.balanceOf(accounts[1], _from(accounts[1]))



	stake_nft(staking, accounts[1], nft, 4)

	# Waiting for second stage
	chain.sleep(arena.firstStageDuration())

	vault_balance = daiToken.balanceOf(vault)

	daiAmount = 10e18
	create_voting_position(voting, daiToken, accounts[2], 1, daiAmount)


	# Second approve and transfer of DAI
	additionalDai = 20e18
	daiToken.approve(voting, additionalDai, _from(accounts[2]))
	voting.addDaiToPosition(1, additionalDai, _from(accounts[2]))

	assert daiToken.balanceOf(accounts[2], _from(accounts[2])) == balance_before - daiAmount - additionalDai
	assert daiToken.balanceOf(vault, _from(accounts[2])) == vault_balance + daiAmount + additionalDai
