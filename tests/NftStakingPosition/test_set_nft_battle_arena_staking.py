import brownie

NULL_ADDRESS = "0x0000000000000000000000000000000000000000"
arena = '0x0000000000000000000000000000000000000042'


def test_set_nft_battle_arena(accounts, NftStakingPosition):
    staking = NftStakingPosition.deploy("name", "symbol", NULL_ADDRESS, NULL_ADDRESS, {"from": accounts[0]})
    staking.setNftBattleArena(arena, {"from": accounts[0]})

    assert staking.nftBattleArena() == arena


def test_owner(accounts, NftStakingPosition):
    staking = NftStakingPosition.deploy("name", "symbol", NULL_ADDRESS, NULL_ADDRESS, {"from": accounts[0]})
    
    with brownie.reverts("Ownable: caller is not the owner"):
        staking.setNftBattleArena(arena, {"from": accounts[1]})


def test_second_setting_of_arena_address(accounts, battles):
    (vault, functions, governance, staking, voting, arena, listing, xZoo, jackpotA, jackpotB) = battles

    with brownie.reverts():
        staking.setNftBattleArena(arena, {"from": accounts[0]})

    
def test_emitting_event(accounts, NftStakingPosition):
    staking = NftStakingPosition.deploy("name", "symbol", NULL_ADDRESS, NULL_ADDRESS, {"from": accounts[0]})

    tx = staking.setNftBattleArena(arena, {"from": accounts[0]})
    
    # Checking "NftBattleArenaSetted" event
    assert len(tx.events) == 1
    assert tx.events[0]["nftBattleArena"] == arena
