import brownie
from brownie import *


def test_weight_calculation_test_values(accounts, listingListForUnitTest_test_values):
	(veZoo, zoo) = listingListForUnitTest_test_values
	zoo.approve(veZoo, 2 ** 256 - 1)

	# setup collections
	collection0 = accounts[-1]
	collection1 = accounts[-2]
	collection2 = accounts[-3]
	collection3 = accounts[-4]

	# batchAllow collections and royalte recipient
	tx1 = veZoo.batchAllowNewContract([collection0, collection1, collection2, collection3], [collection0, collection1, collection2, collection3]) # add collections
	chain.sleep(86500) # skip 1 day+

	# statistics block.
	weight0 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection0) # call weight for 0
	weight1 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection1) # call weight for 1
	weight2 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection2) # call weight for 2
	weight3 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection3) # call weight for 3
	weightTotal = veZoo.updateCurrentEpochAndReturnPoolWeight.call(ZERO_ADDRESS) # call weight total.
	print(weight0, "weight0")
	print(weight1, "weight1")
	print(weight2, "weight2")
	print(weight3, "weight3")
	print(weightTotal, "weightTotal")

	tx = veZoo.updateCurrentEpochAndReturnPoolWeight(collection0)
	assert tx.return_value >= 0

	# vote for 0, Id 1
	tx2 = veZoo.voteForNftCollection(collection0, 1000000000000000000000, veZoo.maxTimelock())
	last_epoch0 = veZoo.lastUpdatedEpochsForCollection(collection0)
	assert veZoo.collectionRecords(collection0, last_epoch0)["rateOfIncrease"] <= veZoo.collectionRecords(collection0, last_epoch0)["decayRate"]
	assert veZoo.collectionRecords(collection0, last_epoch0 + 1)["rateOfIncrease"] <= veZoo.collectionRecords(collection0, last_epoch0 + 1)["decayRate"]
	# vote for 1, Id 2
	tx3 = veZoo.voteForNftCollection(collection1, 1000000000000000000000, veZoo.maxTimelock())
	last_epoch1 = veZoo.lastUpdatedEpochsForCollection(collection1)
	assert veZoo.collectionRecords(collection1, last_epoch1)["rateOfIncrease"] <= veZoo.collectionRecords(collection1, last_epoch1)["decayRate"]
	assert veZoo.collectionRecords(collection1, last_epoch1 + 1)["rateOfIncrease"] <= veZoo.collectionRecords(collection1, last_epoch1 + 1)["decayRate"]

	chain.sleep(3600*6) # skip 6 hours
	# statistics block.
	weight0 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection0) # call weight for 0
	weight1 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection1) # call weight for 1
	weight2 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection2) # call weight for 2
	weight3 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection3) # call weight for 3
	weightTotal = veZoo.updateCurrentEpochAndReturnPoolWeight.call(ZERO_ADDRESS) # call weight total.
	print(weight0, "weight0")
	print(weight1, "weight1")
	print(weight2, "weight2")
	print(weight3, "weight3")
	print(weightTotal, "weightTotal")
	print("collectionRecords")
	print(veZoo.collectionRecords(collection0, last_epoch1))     # collectionRecords for 0
	print(veZoo.collectionRecords(collection0, last_epoch1 + 1)) # collectionRecords for 0
	print(veZoo.collectionRecords(collection1, last_epoch1))     # collectionRecords for 1 
	print(veZoo.collectionRecords(collection1, last_epoch1 + 1)) # collectionRecords for 1

	# vote for 2 id 3
	tx4 = veZoo.voteForNftCollection(collection2, 1000000000000000000000, veZoo.maxTimelock())
	last_epoch2 = veZoo.lastUpdatedEpochsForCollection(collection2)
	assert veZoo.collectionRecords(collection2, last_epoch2)["rateOfIncrease"] <= veZoo.collectionRecords(collection2, last_epoch2)["decayRate"]
	assert veZoo.collectionRecords(collection2, last_epoch2 + 1)["rateOfIncrease"] <= veZoo.collectionRecords(collection2, last_epoch2 + 1)["decayRate"]

	chain.sleep(3700)

	# statistics block.
	print("statistics before prolongate")
	weight0 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection0) # call weight for 0
	weight1 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection1) # call weight for 1
	weight2 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection2) # call weight for 2
	weight3 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection3) # call weight for 3
	weightTotal = veZoo.updateCurrentEpochAndReturnPoolWeight.call(ZERO_ADDRESS) # call weight total.
	print(weight0, "weight0")
	print(weight1, "weight1")
	print(weight2, "weight2")
	print(weight3, "weight3")
	print(weightTotal, "weightTotal")
	print("collectionRecords")
	print(veZoo.collectionRecords(collection0, last_epoch1), "collectionRecords0")     # collectionRecords for 0
	print(veZoo.collectionRecords(collection0, last_epoch1 + 1), "collectionRecords0 epoch+1") # collectionRecords for 0
	print(veZoo.collectionRecords(collection1, last_epoch1), "collectionRecords1")     # collectionRecords for 1 
	print(veZoo.collectionRecords(collection1, last_epoch1 + 1), "collectionRecords1 epoch+1") # collectionRecords for 1
	print(veZoo.collectionRecords(collection2, last_epoch2), "collectionRecords2")
	print(veZoo.collectionRecords(collection2, last_epoch2 + 1), "collectionRecords2 epoch+1") # not zero
	print("end")

	# prolongate for id 3
	tx6 = veZoo.prolongate(1, veZoo.maxTimelock()) # for id3, tx4
	tx6.wait(1)
	last_epoch2 = veZoo.lastUpdatedEpochsForCollection(collection2)
	assert veZoo.collectionRecords(collection2, last_epoch2)["rateOfIncrease"] <= veZoo.collectionRecords(collection2, last_epoch2)["decayRate"]
	assert veZoo.collectionRecords(collection2, last_epoch2 + 1)["rateOfIncrease"] <= veZoo.collectionRecords(collection2, last_epoch2 + 1)["decayRate"]

	# statistics block.
	print("statistics after prolongate")
	weight0 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection0) # call weight for 0
	weight1 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection1) # call weight for 1
	weight2 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection2) # call weight for 2
	weight3 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection3) # call weight for 3
	weightTotal = veZoo.updateCurrentEpochAndReturnPoolWeight.call(ZERO_ADDRESS) # call weight total.
	print(weight0, "weight0")
	print(weight1, "weight1")
	print(weight2, "weight2")
	print(weight3, "weight3")
	print(weightTotal, "weightTotal")
	print(veZoo.getEpochNumber(chain.time()), "epoch number")
	print(veZoo.collectionRecords(collection0, last_epoch1), "collectionRecords0")     # collectionRecords for 0
	print(veZoo.collectionRecords(collection0, last_epoch1 + 1), "collectionRecords0 epoch+1") # collectionRecords for 0
	print(veZoo.collectionRecords(collection1, last_epoch1), "collectionRecords1")     # collectionRecords for 1 
	print(veZoo.collectionRecords(collection1, last_epoch1 + 1), "collectionRecords1 epoch+1") # collectionRecords for 1
	print(veZoo.collectionRecords(collection2, last_epoch2), "collectionRecords2")	
	print(veZoo.collectionRecords(collection2, last_epoch2 + 1), "collectionRecords2 epoch+1") # not zero
	weightCollections = weight0 + weight1 + weight2 + weight3
	assert weightTotal >= weightCollections

	chain.sleep(3600*4)

	print("\nstatistics after prolongate and sleep (before vote)")
	weight0 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection0) # call weight for 0
	weight1 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection1) # call weight for 1
	weight2 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection2) # call weight for 2
	weight3 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection3) # call weight for 3
	weightTotal = veZoo.updateCurrentEpochAndReturnPoolWeight.call(ZERO_ADDRESS) # call weight total.
	print(weight0, "weight0")
	print(weight1, "weight1")
	print(weight2, "weight2")
	print(weight3, "weight3")
	print(weightTotal, "weightTotal")
	print(veZoo.getEpochNumber(chain.time()), "epoch number")
	print(chain.time(), "time")
	print(veZoo.lastUpdatedEpochsForCollection(ZERO_ADDRESS), "lastUpdatedEpochsForCollection for total")
	print(veZoo.lastUpdatedEpochsForCollection(collection3), "veZoo.lastUpdatedEpochsForCollection for collection3")

	weightCollections = weight0 + weight1 + weight2 + weight3
	assert weightTotal >= weightCollections

	# vote for 3 id 4
	tx5 = veZoo.voteForNftCollection(collection3, 1000000000000000000000, veZoo.maxTimelock())
	tx5.wait(1)
	last_epoch3 = veZoo.lastUpdatedEpochsForCollection(collection3)
	assert veZoo.collectionRecords(collection3, last_epoch3)["rateOfIncrease"] <= veZoo.collectionRecords(collection3, last_epoch3)["decayRate"]
	assert veZoo.collectionRecords(collection3, last_epoch3 + 1)["rateOfIncrease"] <= veZoo.collectionRecords(collection3, last_epoch3 + 1)["decayRate"]

	# statistics block.
	print("\nstatistics after prolongate and vote")
	weight0 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection0) # call weight for 0
	weight1 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection1) # call weight for 1
	weight2 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection2) # call weight for 2
	weight3 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection3) # call weight for 3
	weightTotal = veZoo.updateCurrentEpochAndReturnPoolWeight.call(ZERO_ADDRESS) # call weight total.
	print(weight0, "weight0")
	print(weight1, "weight1")
	print(weight2, "weight2")
	print(weight3, "weight3")
	print(weightTotal, "weightTotal")
	print(veZoo.getEpochNumber(chain.time()), "epoch number")
	print(chain.time(), "time")
	print(veZoo.lastUpdatedEpochsForCollection(ZERO_ADDRESS), "lastUpdatedEpochsForCollection for total")
	print(veZoo.lastUpdatedEpochsForCollection(collection3), "veZoo.lastUpdatedEpochsForCollection for collection3")
	print(veZoo.collectionRecords(collection0, last_epoch1), "collectionRecords0")     # collectionRecords for 0
	print(veZoo.collectionRecords(collection0, last_epoch1 + 1), "collectionRecords0 epoch+1") # collectionRecords for 0
	print(veZoo.collectionRecords(collection1, last_epoch1), "collectionRecords1")     # collectionRecords for 1 
	print(veZoo.collectionRecords(collection1, last_epoch1 + 1), "collectionRecords1 epoch+1") # collectionRecords for 1
	print(veZoo.collectionRecords(collection2, last_epoch2), "collectionRecords2")
	print(veZoo.collectionRecords(collection2, last_epoch2 + 1), "collectionRecords2 epoch+1") # not zero
	print(veZoo.collectionRecords(collection3, last_epoch3), "collectionRecords3")
	print(veZoo.collectionRecords(collection3, last_epoch3 + 1), "collectionRecords3 epoch+1")

	tx_upd_1 = veZoo.updateCurrentEpochAndReturnPoolWeight(collection0)
	tx_upd_2 = veZoo.updateCurrentEpochAndReturnPoolWeight(collection1)
	tx_upd_3 = veZoo.updateCurrentEpochAndReturnPoolWeight(collection2)
	tx_upd_4 = veZoo.updateCurrentEpochAndReturnPoolWeight(collection3)
	tx_upd_total = veZoo.updateCurrentEpochAndReturnPoolWeight(ZERO_ADDRESS)

	assert tx_upd_1.return_value == weight0
	assert tx_upd_2.return_value == weight1
	assert tx_upd_3.return_value == weight2
	assert tx_upd_4.return_value == weight3
	assert tx_upd_total.return_value == weightTotal

	weightCollections = weight0 + weight1 + weight2 + weight3

	assert weightTotal >= weightCollections


# def test_weight_calculation_real_values(accounts, listingListForUnitTest):
# 	(veZoo, zoo) = listingListForUnitTest
# 	zoo.approve(veZoo, 2 ** 256 - 1)

# 	day = 86400

# 	# setup collections
# 	collection0 = accounts[-1]
# 	collection1 = accounts[-2]
# 	collection2 = accounts[-3]
# 	collection3 = accounts[-4]
# 	# batchAllow collections and royalte recipient
# 	tx1 = veZoo.batchAllowNewContract([collection0, collection1, collection2, collection3], [collection0, collection1, collection2, collection3]) # add collections

# 	chain.sleep(day * 8) # skip 7 days

# 	# statistics block.
# 	weight0 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection0) # call weight for 0
# 	weight1 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection1) # call weight for 1
# 	weight2 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection2) # call weight for 2
# 	weight3 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection3) # call weight for 3
# 	weightTotal = veZoo.updateCurrentEpochAndReturnPoolWeight.call(ZERO_ADDRESS) # call weight total.
# 	print(weight0, "weight0")
# 	print(weight1, "weight1")
# 	print(weight2, "weight2")
# 	print(weight3, "weight3")
# 	print(weightTotal, "weightTotal")

# 	tx = veZoo.updateCurrentEpochAndReturnPoolWeight(collection0)
# 	assert tx.return_value >= 0

# 	# vote for 0, Id 1
# 	tx2 = veZoo.voteForNftCollection(collection0, 1000000000000000000000, veZoo.maxTimelock())
# 	last_epoch0 = veZoo.lastUpdatedEpochsForCollection(collection0)
# 	assert veZoo.collectionRecords(collection0, last_epoch0)["rateOfIncrease"] <= veZoo.collectionRecords(collection0, last_epoch0)["decayRate"]
# 	assert veZoo.collectionRecords(collection0, last_epoch0 + 1)["rateOfIncrease"] <= veZoo.collectionRecords(collection0, last_epoch0 + 1)["decayRate"]
# 	# vote for 1, Id 2
# 	tx3 = veZoo.voteForNftCollection(collection1, 1000000000000000000000, veZoo.maxTimelock())
# 	last_epoch1 = veZoo.lastUpdatedEpochsForCollection(collection1)
# 	assert veZoo.collectionRecords(collection1, last_epoch1)["rateOfIncrease"] <= veZoo.collectionRecords(collection1, last_epoch1)["decayRate"]
# 	assert veZoo.collectionRecords(collection1, last_epoch1 + 1)["rateOfIncrease"] <= veZoo.collectionRecords(collection1, last_epoch1 + 1)["decayRate"]

# 	chain.sleep(day * 7) # skip
# 	# statistics block.
# 	weight0 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection0) # call weight for 0
# 	weight1 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection1) # call weight for 1
# 	weight2 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection2) # call weight for 2
# 	weight3 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection3) # call weight for 3
# 	weightTotal = veZoo.updateCurrentEpochAndReturnPoolWeight.call(ZERO_ADDRESS) # call weight total.
# 	print(weight0, "weight0")
# 	print(weight1, "weight1")
# 	print(weight2, "weight2")
# 	print(weight3, "weight3")
# 	print(weightTotal, "weightTotal")
# 	print("collectionRecords")
# 	print(veZoo.collectionRecords(collection0, last_epoch1))     # collectionRecords for 0
# 	print(veZoo.collectionRecords(collection0, last_epoch1 + 1)) # collectionRecords for 0
# 	print(veZoo.collectionRecords(collection1, last_epoch1))     # collectionRecords for 1 
# 	print(veZoo.collectionRecords(collection1, last_epoch1 + 1)) # collectionRecords for 1

# 	# vote for 2 id 3
# 	tx4 = veZoo.voteForNftCollection(collection2, 1000000000000000000000, veZoo.maxTimelock())
# 	last_epoch2 = veZoo.lastUpdatedEpochsForCollection(collection2)
# 	assert veZoo.collectionRecords(collection2, last_epoch2)["rateOfIncrease"] <= veZoo.collectionRecords(collection2, last_epoch2)["decayRate"]
# 	assert veZoo.collectionRecords(collection2, last_epoch2 + 1)["rateOfIncrease"] <= veZoo.collectionRecords(collection2, last_epoch2 + 1)["decayRate"]

# 	chain.sleep(day * 3)

# 	# statistics block.
# 	print("statistics before prolongate")
# 	weight0 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection0) # call weight for 0
# 	weight1 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection1) # call weight for 1
# 	weight2 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection2) # call weight for 2
# 	weight3 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection3) # call weight for 3
# 	weightTotal = veZoo.updateCurrentEpochAndReturnPoolWeight.call(ZERO_ADDRESS) # call weight total.
# 	print(weight0, "weight0")
# 	print(weight1, "weight1")
# 	print(weight2, "weight2")
# 	print(weight3, "weight3")
# 	print(weightTotal, "weightTotal")
# 	print("collectionRecords")
# 	print(veZoo.collectionRecords.call(collection0, last_epoch1), "collectionRecords0")     # collectionRecords for 0
# 	print(veZoo.collectionRecords.call(collection0, last_epoch1 + 1), "collectionRecords0 epoch+1") # collectionRecords for 0
# 	print(veZoo.collectionRecords(collection1, last_epoch1), "collectionRecords1")     # collectionRecords for 1 
# 	print(veZoo.collectionRecords(collection1, last_epoch1 + 1), "collectionRecords1 epoch+1") # collectionRecords for 1
# 	print(veZoo.collectionRecords(collection2, last_epoch2), "collectionRecords2")
# 	print(veZoo.collectionRecords(collection2, last_epoch2 + 1), "collectionRecords2 epoch+1") # not zero
# 	# print(veZoo.collectionRecords(collection3, last_epoch3), "collectionRecords3")
# 	# print(veZoo.collectionRecords(collection3, last_epoch3 + 1), "collectionRecords3 epoch+1")
# 	print("end")

# 	# prolongate for id 3
# 	tx6 = veZoo.prolongate(3, veZoo.maxTimelock()) # for id3, tx4
# 	last_epoch2 = veZoo.lastUpdatedEpochsForCollection(collection2)
# 	assert veZoo.collectionRecords(collection2, last_epoch2)["rateOfIncrease"] <= veZoo.collectionRecords(collection2, last_epoch2)["decayRate"]
# 	assert veZoo.collectionRecords(collection2, last_epoch2 + 1)["rateOfIncrease"] <= veZoo.collectionRecords(collection2, last_epoch2 + 1)["decayRate"]

# 	# statistics block.
# 	print("statistics after prolongate")
# 	weight0 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection0) # call weight for 0
# 	weight1 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection1) # call weight for 1
# 	weight2 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection2) # call weight for 2
# 	weight3 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection3) # call weight for 3
# 	weightTotal = veZoo.updateCurrentEpochAndReturnPoolWeight.call(ZERO_ADDRESS) # call weight total.
# 	print(weight0, "weight0")
# 	print(weight1, "weight1")
# 	print(weight2, "weight2")
# 	print(weight3, "weight3")
# 	print(weightTotal, "weightTotal")
# 	print(veZoo.collectionRecords(collection0, last_epoch1), "collectionRecords0")     # collectionRecords for 0
# 	print(veZoo.collectionRecords(collection0, last_epoch1 + 1), "collectionRecords0 epoch+1") # collectionRecords for 0
# 	print(veZoo.collectionRecords(collection1, last_epoch1), "collectionRecords1")     # collectionRecords for 1 
# 	print(veZoo.collectionRecords(collection1, last_epoch1 + 1), "collectionRecords1 epoch+1") # collectionRecords for 1
# 	print(veZoo.collectionRecords(collection2, last_epoch2), "collectionRecords2")
# 	print(veZoo.collectionRecords(collection2, last_epoch2 + 1), "collectionRecords2 epoch+1") # not zero
# 	# print(veZoo.collectionRecords(collection3, last_epoch3), "collectionRecords3")
# 	# print(veZoo.collectionRecords(collection3, last_epoch3 + 1), "collectionRecords3 epoch+1")

# 	chain.sleep(day * 7)

# 	# vote for 3 id 4
# 	tx5 = veZoo.voteForNftCollection(collection3, 1000000000000000000000, veZoo.maxTimelock())
# 	last_epoch3 = veZoo.lastUpdatedEpochsForCollection(collection3)
# 	assert veZoo.collectionRecords(collection3, last_epoch3)["rateOfIncrease"] <= veZoo.collectionRecords(collection3, last_epoch3)["decayRate"]
# 	assert veZoo.collectionRecords(collection3, last_epoch3 + 1)["rateOfIncrease"] <= veZoo.collectionRecords(collection3, last_epoch3 + 1)["decayRate"]

# 	# statistics block.
# 	print("statistics after prolongate and vote")
# 	weight0 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection0) # call weight for 0
# 	weight1 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection1) # call weight for 1
# 	weight2 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection2) # call weight for 2
# 	weight3 = veZoo.updateCurrentEpochAndReturnPoolWeight.call(collection3) # call weight for 3
# 	weightTotal = veZoo.updateCurrentEpochAndReturnPoolWeight.call(ZERO_ADDRESS) # call weight total.
# 	print(weight0, "weight0")
# 	print(weight1, "weight1")
# 	print(weight2, "weight2")
# 	print(weight3, "weight3")
# 	print(weightTotal, "weightTotal")
# 	print(veZoo.collectionRecords(collection0, last_epoch1), "collectionRecords0")     # collectionRecords for 0
# 	print(veZoo.collectionRecords(collection0, last_epoch1 + 1), "collectionRecords0 epoch+1") # collectionRecords for 0
# 	print(veZoo.collectionRecords(collection1, last_epoch1), "collectionRecords1")     # collectionRecords for 1 
# 	print(veZoo.collectionRecords(collection1, last_epoch1 + 1), "collectionRecords1 epoch+1") # collectionRecords for 1
# 	print(veZoo.collectionRecords(collection2, last_epoch2), "collectionRecords2")
# 	print(veZoo.collectionRecords(collection2, last_epoch2 + 1), "collectionRecords2 epoch+1") # not zero
# 	print(veZoo.collectionRecords(collection3, last_epoch3), "collectionRecords3")
# 	print(veZoo.collectionRecords(collection3, last_epoch3 + 1), "collectionRecords3 epoch+1")

# 	weightCollections = weight0 + weight1 + weight2 + weight3
# 	assert weightTotal >= weightCollections
# 	assert False


