# Fifth Challenge: The Rewarder

## Challenge Overview

In this challenge, we aim to address vulnerabilities in the reward distribution mechanism of the protocol, we desire to find a way to get most of the rewards without possessing or supplying any liquidity token for the pool.

### 1. Contracts

- `contracts/the-rewarder/TheRewarderPool.sol`
- `contracts/the-rewarder/RewardToken.sol`
- `contracts/the-rewarder/FlashLoanerPool.sol`
- `contracts/the-rewarder/AccountingToken.sol`
- `contracts/DamnValuableToken.sol`

### 2. Specification

- `contracts/the-rewarder/FifthChallenge.spec`

#### Properties:

- **rewardTokenIncreaseIntegrity**: Ensure the `deposit` and `distributeRewards` functions increase the user reward token balance by the same amount.

## Execution

```bash
certoraRun contracts/the-rewarder/FifthChallenge.conf
```

## Results

[Certora Results](https://vaas-stg.certora.com/output/1512/54e0dbdbee424fd99c4c11f23a56b4fe?anonymousKey=9fe98ce0290bb113227e3d4b9d30b0e739b303b9)

The analysis reveals that the `deposit` function can increase the user reward balance more than the `distributeRewards` function, this vulnerability can be exploit by the user to earn more reward token via `flashloan` thats calls the deposit function in a single transaction.

In order to fix the issue, the order of the reward calculation and balance update should change in the `deposit` function, which will guarantee that the user reward token balance will increase by the same amount for each call:

```solidity
accToken.mint(msg.sender, amountToDeposit);
distributeRewards();
```

changed to:

```solidity
distributeRewards();
accToken.mint(msg.sender, amountToDeposit);
```

### Execution

```bash
certoraRun contracts/the-rewarder/FixedFifthChallenge.conf
```

[Certora Results On Fix Version](https://vaas-stg.certora.com/output/1512/43426ee490a843b980aadfa76240df28?anonymousKey=b7de7543e392cd7f00e6744814b453a109930b0e)
