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
	zoo_token.approve(listingList, value)
	listingList.voteForNftCollection(collection, value, 100 * day)
	epoch_number = listingList.getEpochNumber(time)

	chain.sleep(50 * day)
	listingList.prolongate(1, 100 * day)

def test_prolongate_testnet_values(accounts, listing):
	(listingList, zoo_token) = listing
	collection = accounts[-4]
	recipient = accounts[-5]
	listingList.allowNewContractForStaking(collection, recipient)

	time = chain.time()

	value = 1e21
	zoo_token.approve(listingList, value)
	listingList.voteForNftCollection(collection, value, 86400)
	epoch_number = listingList.getEpochNumber(time)

	chain.sleep(listingList.epochDuration() * 3)
	listingList.prolongate(1, 86400)

def test_multiple_prolongate_testnet_values(accounts, listing):
	(listingList, zoo_token) = listing
	collection = accounts[-4]
	collection1 = accounts[-3]
	recipient = accounts[-5]
	listingList.allowNewContractForStaking(collection, recipient)
	listingList.allowNewContractForStaking(collection1, recipient)

	time = chain.time()

	value = 1e21
	zoo_token.approve(listingList, value)
	listingList.voteForNftCollection(collection, value, 86400)
	zoo_token.approve(listingList, 10e21)
	listingList.voteForNftCollection(collection1, 10e21, 86400)

	chain.sleep(listingList.epochDuration() * 50)
	tx1 = listingList.prolongate(1, 86400)
	tx2 = listingList.prolongate(2, 3600)