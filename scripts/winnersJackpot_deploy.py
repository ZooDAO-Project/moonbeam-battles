from brownie import *


def main():
	active_network = network.show_active()
	account = accounts.load(active_network)

	frax = "0x322E86852e492a7Ee17f28a78c663da38FB33bfb"
	zooToken = "0x1D85202773313B376Ee0F0c83bf0f5cAeC9991D2"
	voting = "0x0837cFd9DFf9f579BA28084ab9d385a1b65fA57c"
	functions = "0x5C28f4ba5a350B9Bbb22660981b24d7b4b4aC805"
	
	fraxReward = 1 * 10 ** 18
	zooReward = 1 * 10 ** 18
	# new lottery contract. last two params are rewards amount for frax and zoo.
	WinnersJackpot.deploy(functions, voting, frax, zooToken, fraxReward, zooReward, {"from": account}, publish_source=True)
