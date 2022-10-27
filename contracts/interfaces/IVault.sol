pragma solidity 0.8.13;
pragma experimental ABIEncoderV2;

// SPDX-License-Identifier: MIT

interface VaultAPI {
	function mint(uint256 mintAmount) external returns (uint256);

	function redeemUnderlying(uint256 redeemAmount, address recipient) external returns (uint256);

	function exchangeRateStored() external view returns (uint);

	function transfer(address who, uint256 amount) external returns (bool);

	function increaseMockBalance() external;
}
