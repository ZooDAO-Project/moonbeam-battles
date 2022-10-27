import brownie

def test_set_constructor_arguments(accounts, NftStakingPosition):
	name = 'Name'
	symbol = 'NM'

	listing = '0x0000000000000000000000000000000000000001'
	zoo = '0x0000000000000000000000000000000000000002'

	staking = NftStakingPosition.deploy(name, symbol, listing, zoo, {"from": accounts[0]})
	
	assert staking.name() == name
	assert staking.symbol() == symbol
	assert staking.listingList() == listing
	assert staking.zoo() == zoo


def test_owner(accounts, NftStakingPosition):
	name = 'Name'
	symbol = 'NM'
	
	listing = '0x0000000000000000000000000000000000000001'
	zoo = '0x0000000000000000000000000000000000000002'

	staking = NftStakingPosition.deploy(name, symbol, listing, zoo, {"from": accounts[9]})
	
	assert staking.owner() == accounts[9]
