#!/usr/bin/python3

import brownie
from brownie import chain

def test_mint(accounts, tokens, testnet):
	(zooToken, daiToken, linkToken, nft) = tokens
	(nft, nft1, nft2, nft3, faucet) = testnet

	# ZooNft = ZooNft.deploy({"from": accounts[0]})
	# ZooNft1 = ZooNft.deploy({"from": accounts[0]})
	# ZooNft2 = ZooNft.deploy({"from": accounts[0]})

	# faucet = ZooTokenFaucet.deploy("name", "symbol", zooToken, daiToken, [ZooNft, ZooNft1, ZooNft2], {"from": accounts[0]})
	print(zooToken.balanceOf(accounts[0]))
	# zooToken.transfer(faucet.address, 4e25, {"from": accounts[0]})
	# daiToken.mint(faucet.address, 4e25, {"from": accounts[0]})

	faucet.getTokens({"from": accounts[0]})

	print(faucet.balanceOf(accounts[0]), "faucet")
	print(nft.balanceOf(accounts[0]), "nft")
	print(nft1.balanceOf(accounts[0]), "nft1")
	print(nft2.balanceOf(accounts[0]), "nft2")
	print(nft3.balanceOf(accounts[0]), "nft3")
	print("_______________")
	print(faucet.balanceOf(faucet), "faucet")
	print(nft.balanceOf(faucet), "nft")
	print(nft1.balanceOf(faucet), "nft1")
	print(nft2.balanceOf(faucet), "nft2")
	print(nft3.balanceOf(faucet), "nft3")

	assert nft.balanceOf(faucet) == 0
	assert nft1.balanceOf(faucet) == 0
	assert nft2.balanceOf(faucet) == 0
	assert nft3.balanceOf(faucet) == 0

