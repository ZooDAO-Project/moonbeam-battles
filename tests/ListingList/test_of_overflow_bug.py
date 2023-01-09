import brownie
from brownie import *


def test_of_overflow_bug(accounts, listingListForUnitTest):
	(veZoo, zoo) = listingListForUnitTest
	collections = accounts[-1:-5:-1]
	zoo.approve(veZoo, 2 ** 256 - 1)
	tx1 = veZoo.batchAllowNewContract(collections, collections)

	collection = collections[1]
	tx = veZoo.updateCurrentEpochAndReturnPoolWeight(collection)
	assert tx.return_value >= 0

	tx2 = veZoo.voteForNftCollection(collection, 1000000000000000000000, veZoo.maxTimelock())
	last_epoch = veZoo.lastUpdatedEpochsForCollection(collection)
	assert veZoo.collectionRecords(collection, last_epoch)["rateOfIncrease"] <= veZoo.collectionRecords(collection, last_epoch)["decayRate"]
	assert veZoo.collectionRecords(collection, last_epoch + 1)["rateOfIncrease"] <= veZoo.collectionRecords(collection, last_epoch + 1)["decayRate"]

	tx = veZoo.updateCurrentEpochAndReturnPoolWeight(collection)
	assert tx.return_value >= 0
	last_epoch = veZoo.lastUpdatedEpochsForCollection(collection)
	assert veZoo.collectionRecords(collection, last_epoch)["rateOfIncrease"] <= veZoo.collectionRecords(collection, last_epoch)["decayRate"]
	assert veZoo.collectionRecords(collection, last_epoch + 1)["rateOfIncrease"] <= veZoo.collectionRecords(collection, last_epoch + 1)["decayRate"]


	tx3 = veZoo.prolongate(1, veZoo.maxTimelock())
	last_epoch = veZoo.lastUpdatedEpochsForCollection(collection)
	assert veZoo.collectionRecords(collection, last_epoch)["rateOfIncrease"] <= veZoo.collectionRecords(collection, last_epoch)["decayRate"]
	assert veZoo.collectionRecords(collection, last_epoch + 1)["rateOfIncrease"] <= veZoo.collectionRecords(collection, last_epoch + 1)["decayRate"]
	
	tx = veZoo.updateCurrentEpochAndReturnPoolWeight(collection)
	assert tx.return_value >= 0
	last_epoch = veZoo.lastUpdatedEpochsForCollection(collection)
	assert veZoo.collectionRecords(collection, last_epoch)["rateOfIncrease"] <= veZoo.collectionRecords(collection, last_epoch)["decayRate"]
	assert veZoo.collectionRecords(collection, last_epoch + 1)["rateOfIncrease"] <= veZoo.collectionRecords(collection, last_epoch + 1)["decayRate"]

	print(last_epoch)
	print(veZoo.collectionRecords(collection, last_epoch))
	print(veZoo.collectionRecords(collection, last_epoch + 1))
	tx4 = veZoo.voteForNftCollection(collection, 80000000000000000000, veZoo.minTimelock() + 60 * 60 * 24 * 7)
	last_epoch = veZoo.lastUpdatedEpochsForCollection(collection)

	print(last_epoch)
	print(veZoo.collectionRecords(collection, last_epoch))
	print(veZoo.collectionRecords(collection, last_epoch + 1))
	assert veZoo.collectionRecords(collection, last_epoch)["rateOfIncrease"] <= veZoo.collectionRecords(collection, last_epoch)["decayRate"]
	assert veZoo.collectionRecords(collection, last_epoch + 1)["rateOfIncrease"] <= veZoo.collectionRecords(collection, last_epoch + 1)["decayRate"]
	tx = veZoo.updateCurrentEpochAndReturnPoolWeight(collection)
	assert tx.return_value >= 0
	last_epoch = veZoo.lastUpdatedEpochsForCollection(collection)
	assert veZoo.collectionRecords(collection, last_epoch)["rateOfIncrease"] <= veZoo.collectionRecords(collection, last_epoch)["decayRate"]
	assert veZoo.collectionRecords(collection, last_epoch + 1)["rateOfIncrease"] <= veZoo.collectionRecords(collection, last_epoch + 1)["decayRate"]

	tx5 = veZoo.voteForNftCollection(collection, 1000000000000000000000, veZoo.minTimelock())
	last_epoch = veZoo.lastUpdatedEpochsForCollection(collection)
	assert veZoo.collectionRecords(collection, last_epoch)["rateOfIncrease"] <= veZoo.collectionRecords(collection, last_epoch)["decayRate"]
	assert veZoo.collectionRecords(collection, last_epoch + 1)["rateOfIncrease"] <= veZoo.collectionRecords(collection, last_epoch + 1)["decayRate"]
	tx = veZoo.updateCurrentEpochAndReturnPoolWeight(collection)
	assert tx.return_value >= 0
	last_epoch = veZoo.lastUpdatedEpochsForCollection(collection)
	assert veZoo.collectionRecords(collection, last_epoch)["rateOfIncrease"] <= veZoo.collectionRecords(collection, last_epoch)["decayRate"]
	assert veZoo.collectionRecords(collection, last_epoch + 1)["rateOfIncrease"] <= veZoo.collectionRecords(collection, last_epoch + 1)["decayRate"]

	chain.sleep(veZoo.maxTimelock())

	tx6 = veZoo.unlockZoo(1)
	last_epoch = veZoo.lastUpdatedEpochsForCollection(collection)
	assert veZoo.collectionRecords(collection, last_epoch)["rateOfIncrease"] <= veZoo.collectionRecords(collection, last_epoch)["decayRate"]
	assert veZoo.collectionRecords(collection, last_epoch + 1)["rateOfIncrease"] <= veZoo.collectionRecords(collection, last_epoch + 1)["decayRate"]
	tx = veZoo.updateCurrentEpochAndReturnPoolWeight(collection)
	assert tx.return_value >= 0
	last_epoch = veZoo.lastUpdatedEpochsForCollection(collection)
	assert veZoo.collectionRecords(collection, last_epoch)["rateOfIncrease"] <= veZoo.collectionRecords(collection, last_epoch)["decayRate"]
	assert veZoo.collectionRecords(collection, last_epoch + 1)["rateOfIncrease"] <= veZoo.collectionRecords(collection, last_epoch + 1)["decayRate"]