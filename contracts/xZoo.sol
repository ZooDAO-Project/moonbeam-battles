pragma solidity 0.8.13;


import "OpenZeppelin/openzeppelin-contracts@4.5.0/contracts/token/ERC20/IERC20.sol";
import "OpenZeppelin/openzeppelin-contracts@4.5.0/contracts/token/ERC721/ERC721.sol";
import "./NftBattleArena.sol";
import "./interfaces/IVault.sol";


contract XZoo is ERC721
{
	struct ZooStakerPosition
	{
		uint256 amount;
		uint256 startEpoch;
		uint256 endEpoch; 
		uint256 yTokensDebt;
	}

	IERC20 public stablecoin;

	IERC20 public zoo;

	VaultAPI public vault;

	NftBattleArena public arena;

	uint256 public indexCounter = 1;

	mapping (uint256 => ZooStakerPosition) public xZooPositions;

	// epoch => total staked zoo
	mapping (uint256 => int256) public totalStakedZoo;

	mapping (address => uint256[]) public tokenOfOwnerByIndex;

	uint256 public lastEpochWhereTotalStakedUpdated;

	event ZooStaked(address indexed staker, address indexed beneficiary, uint256 amount, uint256 positionId);

	event ZooWithdrawal(address indexed staker, address beneficiary, uint256 amount, uint256 positionId);

	event Claimed(address indexed staker, address beneficiary, uint256 amount, uint256 positionId);

	event NftBattleArenaSet(address nftBattleArena);

	constructor (string memory _name, string memory _symbol, address _stablecoin, address _zoo, address _vault) ERC721(_name, _symbol)
	{
		zoo = IERC20(_zoo);
		stablecoin = IERC20(_stablecoin);
		vault = VaultAPI(_vault);
	}

	function setNftBattleArena(address _nftBattleArena) external
	{
		require(address(arena) == address(0));

		arena = NftBattleArena(_nftBattleArena);

		emit NftBattleArenaSet(_nftBattleArena);
	}

	function stakeZoo(uint256 amount, address beneficiary) external returns (uint256 xZooPositionId)
	{
		zoo.transferFrom(msg.sender, address(this), amount);
		xZooPositions[indexCounter].amount = amount;
		xZooPositions[indexCounter].startEpoch = arena.currentEpoch() + 1;
		totalStakedZoo[arena.currentEpoch() + 1] += int256(amount);
		tokenOfOwnerByIndex[beneficiary].push(indexCounter);

		_mint(beneficiary, indexCounter);
		emit ZooStaked(msg.sender, beneficiary, amount, indexCounter);

		return indexCounter++;
	}

	function claimRewards(uint256 positionId, address beneficiary) external returns (uint256 amountOfstablecoins)
	{
		require(ownerOf(positionId) == msg.sender);
		updateTotalStakedUpdated();

		ZooStakerPosition storage position = xZooPositions[positionId];
		uint256 rewards = getPendingReward(positionId);
		position.yTokensDebt = 0;
		position.startEpoch = arena.currentEpoch();

		amountOfstablecoins = vault.redeemUnderlying(rewards, beneficiary);

		emit Claimed(msg.sender, beneficiary, amountOfstablecoins, positionId);
	}

	function unlockZoo(uint256 positionId, address beneficiary) external returns (uint256 amountOfZoo)
	{
		require(ownerOf(positionId) == msg.sender);
		updateTotalStakedUpdated();

		ZooStakerPosition storage position = xZooPositions[positionId];
		require(position.endEpoch == 0);
		position.endEpoch = arena.currentEpoch();
		zoo.transfer(beneficiary, position.amount);
		totalStakedZoo[arena.currentEpoch() + 1] -= int256(position.amount);

		emit ZooWithdrawal(msg.sender, beneficiary, position.amount, positionId);

		return position.amount;
	}

	function unlockAndClaim(uint256 positionId, address beneficiary) external returns (uint256 amountOfZoo, uint256 rewardsForClaimer)
	{
		require(ownerOf(positionId) == msg.sender);
		updateTotalStakedUpdated();

		ZooStakerPosition storage position = xZooPositions[positionId];
		uint256 rewards = getPendingReward(positionId);
		position.yTokensDebt = 0;
		position.startEpoch = arena.currentEpoch();
		uint256 amountOfstablecoins = vault.redeemUnderlying(rewards, beneficiary);
		position.endEpoch = arena.currentEpoch();
		zoo.transfer(beneficiary, position.amount);
		totalStakedZoo[arena.currentEpoch() + 1] -= int256(position.amount);

		emit Claimed(msg.sender, beneficiary, amountOfstablecoins, positionId);
		emit ZooWithdrawal(msg.sender, beneficiary, position.amount, positionId);

		return (position.amount, amountOfstablecoins);
	}

	function addZoo(uint256 positionId, uint256 amount) external
	{
		require(ownerOf(positionId) == msg.sender);
		ZooStakerPosition storage position = xZooPositions[positionId];
		require(position.endEpoch == 0);
		updateTotalStakedUpdated();

		zoo.transferFrom(msg.sender, address(this), amount);

		position.yTokensDebt = getPendingReward(positionId);
		position.startEpoch = arena.currentEpoch();

		position.amount += amount;
		totalStakedZoo[arena.currentEpoch() + 1] += int256(amount);

		emit ZooStaked(msg.sender, ownerOf(positionId), amount, positionId);
	}

	function withdrawZoo(uint256 positionId, uint256 amount, address beneficiary) external
	{
		require(ownerOf(positionId) == msg.sender);
		updateTotalStakedUpdated();

		ZooStakerPosition storage position = xZooPositions[positionId];
		require(position.endEpoch == 0);

		position.yTokensDebt = getPendingReward(positionId);
		position.startEpoch = arena.currentEpoch();

		position.amount -= amount;
		totalStakedZoo[arena.currentEpoch() + 1] -= int256(amount);
		zoo.transfer(beneficiary, amount);

		emit ZooWithdrawal(msg.sender, beneficiary, amount, positionId);
	}

	function updateTotalStakedUpdated() public
	{
		for (uint256 i = lastEpochWhereTotalStakedUpdated + 1; i < arena.currentEpoch(); i++)
		{
			totalStakedZoo[i] += totalStakedZoo[i - 1];
		}
	}

	function getPendingReward(uint256 positionId) public view returns (uint256 yvTokens)
	{
		ZooStakerPosition storage position = xZooPositions[positionId];
		uint256 end = position.endEpoch == 0 ? arena.currentEpoch() : position.endEpoch;
		yvTokens += position.yTokensDebt;

		for (uint256 epoch = position.startEpoch; epoch < end; epoch++)
		{
			yvTokens += position.amount * arena.xZooRewards(epoch) / uint256(totalStakedZoo[epoch]); 
		}
	}
}