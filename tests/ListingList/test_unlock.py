import brownie
from brownie import chain, ZERO_ADDRESS

day = 24 * 60 * 60

def test_unlock(accounts, listingListForUnitTest):
	(listingList, zoo_token) = listingListForUnitTest
	collection = accounts[-4]
	recipient = accounts[-5]
	listingList.allowNewContractForStaking(collection, recipient)
	balance = zoo_token.balanceOf(accounts[0])

	chain.time()

	value = 1e21
	maxTimeLock = listingList.maxTimelock()
	zoo_token.approve(listingList, value)
	listingList.voteForNftCollection(collection, value, maxTimeLock)

	chain.sleep(maxTimeLock)
	listingList.unlockZoo(1)

	assert balance == zoo_token.balanceOf(accounts[0])

