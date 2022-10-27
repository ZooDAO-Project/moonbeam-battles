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
    
    function claimReward(uint8 rewardType, address payable holder) public returns(uint256)
    { // rewardType = 0 for WELL, mToken = address for frax
        require(rewardType == 0, "Incorrect reward type");

        well.transfer(holder, 10 ** 20);

        return 10 ** 20;
    }
}
