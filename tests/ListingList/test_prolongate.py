import brownie
from brownie import chain, ZERO_ADDRESS

day = 24 * 60 * 60

def test_single_prolongate(accounts, listingListForUnitTest):
	(listingList, zoo_token) = listingListForUnitTest
	collection = accounts[-4]
	recipient = accounts[-5]
	listingList.allowNewContractForStaking(collection, recipient)

	time = chain.time()

	value = 1e21
	maxTimeLock = listingList.maxTimelock()
	zoo_token.approve(listingList, value)
	listingList.voteForNftCollection(collection, value, maxTimeLock)
	epoch_number = listingList.getEpochNumber(time)

	chain.sleep(50 * day)
	listingList.prolongate(1, maxTimeLock)

def test_prolongate_testnet_values(accounts, listing):
	(listingList, zoo_token) = listing
	collection = accounts[-4]
	recipient = accounts[-5]
	listingList.allowNewContractForStaking(collection, recipient)

	time = chain.time()

	value = 1e21
	minTimelock = listingList.minTimelock()
	zoo_token.approve(listingList, value)
	listingList.voteForNftCollection(collection, value, minTimelock)
	epoch_number = listingList.getEpochNumber(time)

	chain.sleep(listingList.epochDuration() * 3)
	listingList.prolongate(1, minTimelock)

def test_multiple_prolongate_testnet_values(accounts, listing):
	(listingList, zoo_token) = listing
	collection = accounts[-4]
	collection1 = accounts[-3]
	recipient = accounts[-5]
	listingList.allowNewContractForStaking(collection, recipient)
	listingList.allowNewContractForStaking(collection1, recipient)

	time = chain.time()

	value = 1e21
	minTimelock = listingList.minTimelock()
	maxTimeLock = listingList.maxTimelock()
	zoo_token.approve(listingList, value)
	listingList.voteForNftCollection(collection, value, maxTimeLock)
	zoo_token.approve(listingList, 10e21)
	listingList.voteForNftCollection(collection1, 10e21, maxTimeLock)

	chain.sleep(listingList.epochDuration() * 50)
	tx1 = listingList.prolongate(1, minTimelock)
	tx2 = listingList.prolongate(2, maxTimeLock)