import brownie
from brownie import chain

def test_add_dai_to_voting_for_same_position_in_second_epoch(finished_epoch, accounts):
	(zooToken, daiToken, linkToken, nft) = finished_epoch[0]
	(vault, functions, governance, staking, voting, arena, listing, xZoo, jackpotA, jackpotB) = finished_epoch[1]

	chain.sleep(arena.firstStageDuration())

	voting_position_id = 1

	dai_amount = 50 * 10 ** 18

	tx = voting.addDaiToPosition(voting_position_id, dai_amount, {"from": accounts[0]})