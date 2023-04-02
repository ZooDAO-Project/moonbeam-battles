from brownie import *

def main():
	active_network = network.show_active()
	account = accounts.load(active_network)

	vault = "0x1C55649f73CDA2f72CEf3DD6C5CA3d49EFcF484C"
	frax = "0x322E86852e492a7Ee17f28a78c663da38FB33bfb"
	token_controller = "0x8E00D5e02E65A19337Cdba98bbA9F84d4186a180"
	well = "0x511aB53F793683763E5a8829738301368a2411E3"
	wGlmr = "0xAcc15dC74880C9944775448304B263D191c6077F"
	zooToken = "0x7cd3e6e1A69409deF0D78D17a492e8e143F40eC5"

	day = 60 * 60 * 24
	firstStageDuration = 2 * day
	secondStageDuration = 5 * day
	thirdStageDuration = 1 * day
	fourthStageDuration = 12 * day
	fifthStageDuration = 1 * day

	functions = BaseZooFunctions.deploy(ZERO_ADDRESS, ZERO_ADDRESS, firstStageDuration, secondStageDuration, thirdStageDuration, fourthStageDuration, fifthStageDuration, {"from": account}, publish_source=True)

	governance = ZooGovernance.deploy(functions, account, {"from": account}, publish_source=True)
	ve_zoo = ListingList.deploy(zooToken, 1814400, 1814400, 7257600, 7257600, {"from": account}, publish_source=True) # 21 day, 84 day

	staking = NftStakingPosition.deploy("zStakerPosition", "ZSP", ve_zoo, zooToken, {"from": account}, publish_source=True)
	voting = NftVotingPosition.deploy("zVoterPosition", "ZVP",
		frax, # frax
		zooToken, # zoo token/mock
		{"from": account}, publish_source=True)

	x_zoo = XZoo.deploy("xZoo", "XZOO", frax, zooToken, vault, {"from": account}, publish_source=True)
	iterable_mapping = IterableMapping.deploy({"from": account}, publish_source=True) # ???

	jackpot_a = Jackpot.deploy(staking, vault, functions, "Jackpot A", "JKPTA", {"from": account}, publish_source=True)
	jackpot_b = Jackpot.deploy(voting, vault, functions, "Jackpot B", "JKPTB", {"from": account}, publish_source=True)

	arena = NftBattleArena.deploy(
		zooToken, # zoo token/mock
		frax, # frax
		vault, 
		governance,
		"0x77A571d87C7BD06274493d144a7C678A397a13cc",                                              # treasury pool
		#"0x24410c1d93d1216E126b6A6cd32d79f634308b3b",                                              # gas fee pool      address/mock
		"0x24410c1d93d1216E126b6A6cd32d79f634308b3b",                                              # team
		staking,
		voting, 
		ve_zoo,
		token_controller,
		well,
		{"from": account}, publish_source=True)
	
	# new lottery contract.
	winnersJackpot = WinnersJackpot.deploy(functions, voting, frax, zooToken, {"from": account}, publish_source=True)

	arena.init(x_zoo, jackpot_a, jackpot_b, wGlmr)
	x_zoo.setNftBattleArena(arena)
	jackpot_a.setNftBattleArena(arena)
	jackpot_b.setNftBattleArena(arena)

	staking.setNftBattleArena(arena, {"from": account})
	voting.setNftBattleArena(arena, {"from": account})
	functions.init(arena, account, {"from": account})

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