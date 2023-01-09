import brownie
from brownie import chain, ZERO_ADDRESS

def test_single_vote(accounts, listing):
	(listingList, zoo_token) = listing
	collection = accounts[-4]
	recipient = accounts[-5]
	listingList.allowNewContractForStaking(collection, recipient)

	time = chain.time()

	value = 1e21
	zoo_token.approve(listingList, value)
	listingList.voteForNftCollection(collection, value, listingList.maxTimelock() // 2)
	epoch_number = listingList.getEpochNumber(time)
	record_for_collection = listingList.collectionRecords(collection, epoch_number + 1)

	assert record_for_collection["rateOfIncrease"] == 0
	#assert record_for_collection["weightAtTheStart"] == (value * 100 * day) // listingList.maxTimelock() # should to be equal. WTF
	assert record_for_collection["decayRate"] == record_for_collection["weightAtTheStart"] // (listingList.maxTimelock() // 2)


	record_for_total = listingList.collectionRecords(ZERO_ADDRESS, epoch_number + 1)

	assert record_for_total["rateOfIncrease"] == 0
	#assert record_for_total["weightAtTheStart"] == (value * 100 * day) // listingList.maxTimelock() # should to be equal. WTF
	assert record_for_total["decayRate"] == record_for_total["weightAtTheStart"] // (listingList.maxTimelock() // 2)

	epoch_number_of_expiration = listingList.getEpochNumber(time + listingList.maxTimelock() // 2)
	record_for_collection_at_expiration = listingList.collectionRecords(collection, epoch_number_of_expiration)
	assert record_for_collection["decayRate"] == record_for_collection_at_expiration["rateOfIncrease"]

	record_for_total_at_expiration = listingList.collectionRecords(ZERO_ADDRESS, epoch_number_of_expiration)
	assert record_for_total["decayRate"] == record_for_total_at_expiration["rateOfIncrease"]

	# to next test
	#assert listingList.getVectorForEpoch(collection, epoch_number) == record_for_collection["decayRate"]
	#assert listingList.getVectorForEpoch(ZERO_ADDRESS, epoch_number) == record_for_total["decayRate"]

def test_multi_vote_in_one_epoch(accounts, listing):
	(listingList, zoo_token) = listing
	collection = accounts[-4]
	recipient = accounts[-5]
	listingList.allowNewContractForStaking(collection, recipient)

	time = chain.time()
	value1 = 1e21
	zoo_token.approve(listingList, value1)
	listingList.voteForNftCollection(collection, value1, listingList.maxTimelock() // 2)
	epoch_number = listingList.getEpochNumber(time)
	epoch_number_of_expiration = listingList.getEpochNumber(time + listingList.maxTimelock() // 2)
	record_for_collection1 = listingList.collectionRecords(collection, epoch_number + 1)
	record_for_total1 = listingList.collectionRecords(ZERO_ADDRESS, epoch_number + 1)
	record_for_collection_at_expiration1 = listingList.collectionRecords(collection, epoch_number_of_expiration)
	record_for_total_at_expiration1 = listingList.collectionRecords(ZERO_ADDRESS, epoch_number_of_expiration)

	zoo_token.approve(listingList, value1 * 2)
	listingList.voteForNftCollection(collection, value1 * 2, listingList.maxTimelock() // 2)
	record_for_collection2 = listingList.collectionRecords(collection, epoch_number + 1)
	record_for_total2 = listingList.collectionRecords(ZERO_ADDRESS, epoch_number + 1)
	record_for_collection_at_expiration2 = listingList.collectionRecords(collection, epoch_number_of_expiration)
	record_for_total_at_expiration2 = listingList.collectionRecords(ZERO_ADDRESS, epoch_number_of_expiration)

	assert record_for_collection2["decayRate"] > record_for_collection1["decayRate"]
	assert record_for_total2["decayRate"] > record_for_total1["decayRate"]
	assert record_for_collection_at_expiration2["rateOfIncrease"] > record_for_collection_at_expiration1["rateOfIncrease"]
	assert record_for_total_at_expiration2["rateOfIncrease"] > record_for_total_at_expiration1["rateOfIncrease"]
	assert record_for_collection2["rateOfIncrease"] <= record_for_collection2["decayRate"]
	assert record_for_total2["rateOfIncrease"] <= record_for_total2["decayRate"]