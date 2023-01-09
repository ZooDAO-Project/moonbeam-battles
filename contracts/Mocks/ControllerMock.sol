pragma solidity 0.8.13;

// SPDX-License-Identifier: MIT
import "OpenZeppelin/openzeppelin-contracts@4.7.3/contracts/token/ERC20/ERC20.sol";

contract ControllerMock
{
	ERC20 public well;                      // well token interface

	constructor(address _well) 
	{
		well = ERC20(_well);
	}

	receive() external payable {}

	function claimReward(uint8 rewardType, address payable holder) public
	{ // rewardType = 0 for WELL, mToken = address for frax
		require(rewardType <= 1, "Incorrect reward type");
		if (rewardType == 0) {
			well.transfer(holder, 10 ** 20);
		} else {
			holder.transfer(address(this).balance / 2);
		}
	}
}
