import brownie
from brownie import chain


def _from(account):
	return {"from": account}

# copied from test_shares_to_tokens.py
# def test_return_shares_according_to_vault(accounts, fifth_stage):
# 	(zooToken, daiToken, linkToken, nft) = fifth_stage[0]
# 	(vault, functions, governance, staking, voting, arena, listing) = fifth_stage[1]
	
# 	sharesAmount = 1e18
# 	pps = vault.pricePerShare()
# 	tokensDecimals = daiToken.decimals()

# 	expectedValue = sharesAmount * pps / (10 ** tokensDecimals)
# 	assert arena.sharesToTokens(sharesAmount) == expectedValue


# def test_stress(accounts, fifth_stage):
# 	(zooToken, daiToken, linkToken, nft) = fifth_stage[0]
# 	(vault, functions, governance, staking, voting, arena, listing) = fifth_stage[1]
	
# 	print(daiToken.balanceOf(vault))
# 	for i in range(37):
# 		sharesAmount = 10 ** (18 + i)
# 		print(i, sharesAmount)
# 		pps = vault.pricePerShare()
# 		tokensDecimals = daiToken.decimals()

# 		expectedValue = sharesAmount * pps / (10 ** tokensDecimals)
# 		assert arena.sharesToTokens(sharesAmount) == expectedValue

# new tests below.

# def test_shareValue_equal_to_sharesToTokens(accounts, fifth_stage):
# 	(zooToken, daiToken, linkToken, nft) = fifth_stage[0]
# 	(vault, functions, governance, staking, voting, arena, listing) = fifth_stage[1]
# 	amount = 100e18
# 	amount1 = 20e18
# 	amount2 = 8e18

# 	daiToken.approve(vault.address, amount*2)
# 	vault.mint(amount)
# 	vault.redeemUnderlying(amount1, accounts[1])

# 	shares = 20000000000000000000
# 	pps = vault.exchangeRateStored()
	

# 	assert True
