from brownie import *


def main():
	active_network = network.show_active()
	account = accounts.load(active_network)

	frax = "0x322E86852e492a7Ee17f28a78c663da38FB33bfb"
	zooToken = "0x7cd3e6e1A69409deF0D78D17a492e8e143F40eC5"
	voting = "0x54F37fFF3C9652bBEe3Ca3dd72ab619152F1b2D9"
	functions = "0x4510AB2E7ACD55bF792c15F0537f8a25661D0bb5"

	WinnersJackpot.deploy(functions, voting, frax, zooToken, {"from": account}, publish_source=True)
