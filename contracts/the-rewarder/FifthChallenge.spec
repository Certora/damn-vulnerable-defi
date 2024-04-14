using FlashLoanerPool as flashloan;
using RewardToken as rewardToken;

/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Deposit increase reward token balance with the same amount as distribute rewards                                                    │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/
rule rewardTokenIncreaseIntegrity()
{
    env e;
    address user;
    uint256 amount;

    storage init = lastStorage;

    distributeRewards(e);
    uint256 balanceAfterDistributeRewards = rewardToken.balanceOf(e, user);
    
    deposit(e, amount) at init;
    uint256 balanceAfterDeposit = rewardToken.balanceOf(e, user);
    
    assert balanceAfterDistributeRewards == balanceAfterDeposit;
}