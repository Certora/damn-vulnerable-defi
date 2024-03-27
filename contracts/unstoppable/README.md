# First Challenge: Halting Flash Loans

## Challenge Overview

In this challenge, we aim to address vulnerabilities in a tokenized vault that offers free flash loans until a grace period ends. The primary objective is to deactivate the vault's ability to provide flash loans.

### 1. Contracts

- `contracts/unstoppable/ReceiverUnstoppable.sol`
- `contracts/unstoppable/UnstoppableLender.sol`
- `contracts/DamnValuableToken.sol`

### 2. Specification

- `contracts/unstoppable/FirstChallenge.spec`

#### Example Specifications:

- **Reachability**: Ensures all contract methods are accessible and executable as intended.
- **Flash Loan Denial of Service**: Identifies vulnerabilities related to flash loans, demonstrating how an attacker could revert flash loans, thus denying service to legitimate users.

## Execution

```bash
certoraRun contracts/unstoppable/FirstChallenge.conf
```

## Results

[Certora Results](https://prover.certora.com/output/1512/1b14f7e64fd841cdba46e160a5c418ab?anonymousKey=12bee694f43bafa5df07abcb788fa65cb9d68130)

The analysis reveals that the attacker can directly send DVT tokens to the lender contract (or use `transferFrom`), causing the `balanceBefore` assertion to consistently fail due to the `poolBalance` variable not being updated. This exploit renders flash loans unusable.

In order to fix the issue, the assert condition is modified from:

```solidity
assert(poolBalance == balanceBefore);
```

To:

```solidity
assert(poolBalance <= balanceBefore);
```

### Execution

```bash
certoraRun contracts/unstoppable/FixedFirstChallenge.conf
```

[Certora Results On Fix Version](https://prover.certora.com/output/1512/2626b553ef404f9aad184b26d94da7e7?anonymousKey=f0c5da4e4c56ee4eb5fbd6359bfa092c563fb97a)