import brownie
from brownie import chain


def _from(account):
	return {"from": account}


def test_return_shares_according_to_vault(accounts, fifth_stage):
	(zooToken, daiToken, linkToken, nft) = fifth_stage[0]
	(vault, functions, governance, staking, voting, arena, listing, xZoo, jackpotA, jackpotB) = fifth_stage[1]
	
	sharesAmount = 1e18
	pps = vault.exchangeRateStored()
	tokensDecimals = daiToken.decimals()

	expectedValue = sharesAmount * pps / (10 ** tokensDecimals)
	assert arena.sharesToTokens(sharesAmount) == expectedValue


def test_stress(accounts, fifth_stage):
	(zooToken, daiToken, linkToken, nft) = fifth_stage[0]
	(vault, functions, governance, staking, voting, arena, listing, xZoo, jackpotA, jackpotB) = fifth_stage[1]
	
	print(daiToken.balanceOf(vault))
	for i in range(37):
		sharesAmount = 10 ** (18 + i)
		print(i, sharesAmount)
		pps = vault.exchangeRateStored()
		tokensDecimals = daiToken.decimals()
		
		expectedValue = sharesAmount * pps / (10 ** tokensDecimals)
		assert arena.sharesToTokens(sharesAmount) == expectedValue
