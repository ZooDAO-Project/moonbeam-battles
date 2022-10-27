import brownie
from brownie import chain, ZERO_ADDRESS

day = 24 * 60 * 60

def test_single_update(accounts, listingListForUnitTest):
	(listingList, zoo_token) = listingListForUnitTest
	
	#currentEpoch = listingList.getEpochNumber(chain.time())
	listingList.updateCurrentEpochAndReturnPoolWeight(ZERO_ADDRESS)
	record = listingList.collectionRecords(ZERO_ADDRESS, 1)


def test_deep_update(accounts, listingListForUnitTest):
	(listingList, zoo_token) = listingListForUnitTest
	
	#currentEpoch = listingList.getEpochNumber(chain.time())
	chain.sleep(listingList.epochDuration() * 200)
	listingList.updateCurrentEpochAndReturnPoolWeight(ZERO_ADDRESS)
	
	assert listingList.lastUpdatedEpochsForCollection(ZERO_ADDRESS) == 201


def test_update_current_epoch(accounts, listingListForUnitTest):
	(listingList, zoo_token) = listingListForUnitTest
	
	skip = 100 * day
	chain.sleep(skip)
	current_epoch = listingList.getEpochNumber(chain.time())
	listingList.updateCurrentEpochAndReturnPoolWeight(ZERO_ADDRESS)

	assert listingList.lastUpdatedEpochsForCollection(ZERO_ADDRESS) == current_epoch

def test_update_current_epoch_after_weight_became_zero(accounts, listingListForUnitTest):
	(listingList, zoo_token) = listingListForUnitTest
	
	skip = 400 * day
	chain.sleep(skip)
	current_epoch = listingList.getEpochNumber(chain.time())
	tx = listingList.updateCurrentEpochAndReturnPoolWeight(ZERO_ADDRESS)

	assert tx.return_value == 0
	assert listingList.poolWeight(ZERO_ADDRESS, current_epoch) == 0