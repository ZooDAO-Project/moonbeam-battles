import brownie
from brownie import chain


def _from(account):
	return {"from": account}


def test_return_shares_according_to_vault(accounts, fifth_stage):
	(zooToken, daiToken, linkToken, nft) = fifth_stage[0]
	(vault, functions, governance, staking, voting, arena, listing, xZoo, jackpotA, jackpotB) = fifth_stage[1]
	
	tokensAmount = 1e18
	pps = vault.exchangeRateStored()
	tokensDecimals = daiToken.decimals()

	expectedValue = tokensAmount * (10 ** tokensDecimals) / pps
	assert arena.tokensToShares(tokensAmount) == expectedValue


def test_stress(accounts, fifth_stage):
	(zooToken, daiToken, linkToken, nft) = fifth_stage[0]
	(vault, functions, governance, staking, voting, arena, listing, xZoo, jackpotA, jackpotB) = fifth_stage[1]

	for i in range(8):
		sharesAmount = 10 ** (18 + i)
		pps = vault.exchangeRateStored()
		tokensDecimals = daiToken.decimals()
		
		expectedValue = sharesAmount * (10 ** tokensDecimals) / pps
		assert arena.tokensToShares(sharesAmount) == expectedValue
