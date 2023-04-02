from brownie import *


def main():
	active_network = network.show_active()
	account = accounts.load(active_network)
	treasury = "0x24410c1d93d1216E126b6A6cd32d79f634308b3b"

	vault = "0x1C55649f73CDA2f72CEf3DD6C5CA3d49EFcF484C"
	frax = "0x322E86852e492a7Ee17f28a78c663da38FB33bfb"
	token_controller = "0x8E00D5e02E65A19337Cdba98bbA9F84d4186a180"
	well = "0x511aB53F793683763E5a8829738301368a2411E3"
	wGlmr = "0xAcc15dC74880C9944775448304B263D191c6077F"
	zooToken = "0x3907e6ff436e2b2B05D6B929fb05F14c0ee18d90"

	collections = ["0x8fBE243D898e7c88A6724bB9eB13d746614D23d6", "0x139e9BA28D64da245ddB4cF9943aA34f6d5aBFc5", "0x2159762693C629C5A44Fc9baFD484f8B96713467", "0x02A6DeC99B2Ca768D638fcD87A96F6069F91287c", "0x87C359d86bD8C794124090A82E0930c3Cab88F01"]
	royalty = [treasury, treasury, treasury, treasury, treasury]

	attemptsAmount = 1 # attempt limit for calling functions like for get tokens or get nfts.
	faucet = ZooTokenFaucet.deploy(zooToken, attemptsAmount, {"from": account}, publish_source=True) # faucet

	# addresses for whiteList in case they need to change something or take more tokens.
	# TrevorAddress = "0x7f8ff0898d51D0B515868585F09a338e42b0CBa1" # need to fill his address.
	# JoshAddress = "0x7f8ff0898d51D0B515868585F09a338e42b0CBa1"   # need to fill his address.
	# RhinatAddress = "0x7f8ff0898d51D0B515868585F09a338e42b0CBa1" # need to fill his address.

	alexeyAddress = "0x7f8ff0898d51D0B515868585F09a338e42b0CBa1" # and for me in case would need something to change instead of them.
	faucet.batchAddToWhiteList([alexeyAddress], {"from": account})

	# zooToken.mint(faucet.address, 5e26)
	# zooToken.mint(account, 1e26)
	# zooToken.mint("0x4122691B0dd344b3CCd13F4Eb8a71ad22c8CCe5c", 5e26)
	# zooToken.mint("0xaB90ff4a66b9727158C3422770b450d7Ca9011B1", 5e26)
	# zooToken.mint("0x47515585ef943F8E56C17BA0f50fb7E28CE1c4Dc", 5e26)
	# zooToken.mint("0x804b8ff3b23b319208ab5e4053a02a2ba0364430", 5e26)
	# zooToken.mint("0x5232f14c6969102c1afda0c8d81758ea638c0a3b", 5e26)
	# zooToken.mint("0x9498af223fa03a0ea9247bfb330600eec2ddc23b", 5e26)

	day = 60 * 60 * 24
	firstStageDuration = 2 * day
	secondStageDuration = 5 * day
	thirdStageDuration = 1 * day
	fourthStageDuration = 12 * day
	fifthStageDuration = 1 * day

	functions = BaseZooFunctions.deploy(ZERO_ADDRESS, ZERO_ADDRESS, firstStageDuration, secondStageDuration, thirdStageDuration, fourthStageDuration, fifthStageDuration, {"from": account}, publish_source=True)
	functions.setStageDuration(0, 60 * 20, {"from": account}) # 1 stage - 20 mins
	functions.setStageDuration(1, 60 * 20, {"from": account}) # 2 stage - 20 mins
	functions.setStageDuration(2, 60 * 20, {"from": account}) # 3 stage - 20 mins
	functions.setStageDuration(3, 60 * 20, {"from": account}) # 4 stage - 20 mins
	functions.setStageDuration(4, 60 * 20, {"from": account}) # 5 stage - 20 mins
	governance = ZooGovernance.deploy(functions, account, {"from": account}, publish_source=True)

	duration_of_incentive_rewards = 60 * 20 * 5 * 96 # 96 epoch duration of arena
	ve_zoo = ListingList.deploy(zooToken, 6000, 6000, 24000, duration_of_incentive_rewards, {"from": account}, publish_source=True)

	staking = NftStakingPosition.deploy("zStakerPosition", "ZSP", ve_zoo, zooToken, {"from": account}, publish_source=True)
	voting = NftVotingPosition.deploy("zVoterPosition", "ZVP",
		frax, # frax
		zooToken, # zoo token/mock
		{"from": account}, publish_source=True)

	x_zoo = XZoo.deploy("xZoo", "XZOO", frax, zooToken, vault, {"from": account}, publish_source=True)
	iterable_mapping = IterableMapping.deploy({"from": account}, publish_source=True)
	jackpot_a = Jackpot.deploy(staking, vault, functions, "Jackpot A", "JKPTA", {"from": account}, publish_source=True)
	jackpot_b = Jackpot.deploy(voting, vault, functions, "Jackpot B", "JKPTB", {"from": account}, publish_source=True)

	arena = NftBattleArena.deploy(
		zooToken, # zoo token/mock
		frax, # frax
		vault, 
		governance,
		"0x77A571d87C7BD06274493d144a7C678A397a13cc",                                              # treasury pool     address/mock
		#"0x24410c1d93d1216E126b6A6cd32d79f634308b3b",                                              # gas fee pool      address/mock
		"0x24410c1d93d1216E126b6A6cd32d79f634308b3b",                                              # team              address/mock
		staking,
		voting, 
		ve_zoo,
		token_controller,
		well,
		{"from": account}, publish_source=True)

	# new lottery contract. last two params are rewards amount for frax and zoo.
	winnersJackpot = WinnersJackpot.deploy(functions, voting, frax, zooToken, 10**18, 10**18, {"from": account}, publish_source=True)

	arena.init(x_zoo, jackpot_a, jackpot_b, wGlmr)
	x_zoo.setNftBattleArena(arena)
	jackpot_a.setNftBattleArena(arena)
	jackpot_b.setNftBattleArena(arena)

	staking.setNftBattleArena(arena, {"from": account})
	voting.setNftBattleArena(arena, {"from": account})
	functions.init(arena, account, {"from": account})        # connect functions with battleStaker and set owner(should be aragon in mainnet)

	ve_zoo.batchAllowNewContract(collections, royalty, {"from": account})

	# number_of_epochs = duration_of_incentive_rewards // ve_zoo.epochDuration() + 1
	# number_of_zoo_for_incentive_rewards_of_stakers = number_of_epochs * arena.baseStakerReward()
	# number_of_zoo_for_incentive_rewards_of_voters = number_of_epochs * arena.baseVoterReward()
	# zooToken.mint(staking, number_of_zoo_for_incentive_rewards_of_stakers, {"from": account})
	# zooToken.mint(voting, number_of_zoo_for_incentive_rewards_of_voters, {"from": account})

	result = {
		"token" : frax,
		"vault" : vault,
		"token_controller": token_controller,
		"well" : well,
		"wGlmr" : wGlmr,
		"zooToken" : zooToken,
		"collections" : collections,
		"faucet" : faucet,
		"functions" : functions,
		"governance" : governance,
		"ve_zoo" : ve_zoo,
		"staking" : staking,
		"voting" : voting,
		"x_zoo" : x_zoo,
		"jackpot_a" : jackpot_a,
		"jackpot_b" : jackpot_b,
		"arena" : arena,
		"winnersJackpot" : winnersJackpot
	}

	return result