pragma solidity 0.8.13;


import "OpenZeppelin/openzeppelin-contracts@4.5.0/contracts/token/ERC20/presets/ERC20PresetMinterPauser.sol";


contract Token is ERC20PresetMinterPauser
{
	constructor (string memory _name, string memory _symbol) ERC20PresetMinterPauser(_name, _symbol)
	{

	}
}