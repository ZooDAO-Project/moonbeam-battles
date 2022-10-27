pragma solidity 0.8.13;

// SPDX-License-Identifier: MIT

import "../interfaces/IVault.sol";
import "OpenZeppelin/openzeppelin-contracts@4.5.0/contracts/token/ERC20/ERC20.sol";

contract YearnMock is ERC20
{

	ERC20 public frax;                      // frax token interface

	uint256 public mockBalance;
	uint256 public lastDate;
	uint256 public timeDelay = 300;

	event IncreasedBalance(uint256 amount, uint256 lastDate, address user);
	event Withdrawed(uint256 shares, uint256 withdrawn, address receiver);
	event Deposited(uint256 amount, uint256 shares, address user);

	constructor(address _frax) ERC20("yToken", "YTN")
	{
		frax = ERC20(_frax);
	}

	function exchangeRateStored() public view returns (uint256) 
	{
		if (mockBalance == 0 || totalSupply() == 0)
		{
			return 10**18;
		}
		else
		{
			return mockBalance * (10**18) / (totalSupply());
		}
	}

	/// @notice Function to convert yTokens to frax
	/// @param numShares - amount of yTokens
	function _shareValue(uint256 numShares) public view returns (uint256)
	{
		if (totalSupply() > 0)
		{
			return mockBalance * (numShares) / (totalSupply());
		}
		else
		{
			return numShares;
		}
	}

	/// @notice function to convert frax to yTokens.
	/// @param amount - amount of frax.
	function _sharesForValue(uint256 amount) public view returns (uint256)
	{
		if (totalSupply() > 0)
		{
			return amount * 10**18 / exchangeRateStored();
		}
		else
		{
			return amount;
		}
	}

	/// @param amount - amount of frax.
	/// @return shares - amount of yTokens.
	function mint(uint256 amount) public returns (uint256 shares)
	{
		shares = _sharesForValue(amount);  // convert frax to yTokens.

		frax.transferFrom(msg.sender, address(this), amount);

		_mint(msg.sender, shares);

		mockBalance += amount;

		emit Deposited(amount, shares, msg.sender);

		return shares;
	}

	/// @param shares - amount of yTokens
	/// @return withdrawn - amount of frax.
	function redeemUnderlying(uint256 shares, address receiver) public returns (uint256 withdrawn)
	{
		withdrawn = _shareValue(shares); // convert yTokens to frax.

		_burn(msg.sender, shares);

		frax.transfer(receiver, withdrawn);

		mockBalance -= withdrawn;

		emit Withdrawed(shares, withdrawn, receiver);

		return withdrawn;
	}
/*
	/// @param fraxNumber - amount of frax
	/// @return shares - amount of yTokens
	function withdrawTokens(uint256 fraxNumber, address receiver) public override returns (uint256 shares) {
		shares = _sharesForValue(fraxNumber);  // convert frax to yTokens.

		_burn(msg.sender, shares);

		frax.transfer(receiver, fraxNumber);

		mockBalance -= fraxNumber;

		emit Withdrawed(shares, fraxNumber, receiver);

		return fraxNumber;
	}
*/
	function increaseMockBalance() external
	{
		// uint256 increaseLimit = mockBalance * 10 / 100;
		uint256 amount = mockBalance * 10 / 100;
		// require(amount <= increaseLimit, "transfer amount too hight");
		require(block.timestamp > lastDate + timeDelay, "transfer has been recently");

		// frax.transferFrom(msg.sender, address(this), amount);

		mockBalance += amount;
		lastDate = block.timestamp;

		emit IncreasedBalance(amount, lastDate, msg.sender);
	}
}
