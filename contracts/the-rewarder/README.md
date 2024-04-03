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

#### Example Specifications:

- **DepositCantBeInvokedByFlashLoan**: Ensure the `deposit` function is protected against flashloan attack.

## Execution

```bash
certoraRun contracts/the-rewarder/FifthChallenge.conf
```

## Results

[Certora Results](https://vaas-stg.certora.com/output/1512/3af3642d5e724ddb9d3eee1812284fed?anonymousKey=b9b4bb00a48450f176f1a28dc5f09298d17fbbe9)

The analysis reveals that the attacker can use the flash loan to deposit loaned DVT tokens to the reward poll contract and get an account token which then can be used to be eligible for the reward token distribution, in the same transaction the attacker can also call the `withdraw` function to pay back the loan.

In order to fix the issue, another `require` should be added to the `deposit` function
which will guarantee that the depositor user is not a flash loan contract:

```solidity
require(!Address.isContract(msg.sender));
```

### Execution

```bash
certoraRun contracts/the-rewarder/FixedFifthChallenge.conf
```

will be green after the fix of https://certora.atlassian.net/browse/CERT-5732

[Certora Results On Fix Version](https://prover.certora.com/output/1512/2626b553ef404f9aad184b26d94da7e7?anonymousKey=f0c5da4e4c56ee4eb5fbd6359bfa092c563fb97a)
