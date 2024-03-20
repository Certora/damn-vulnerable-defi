# First Challenge

## Challenge #1 - Halting Flash Loans

In this challenge, there's a tokenized vault housing a million DVT tokens, currently offering free flash loans until a grace period ends. The task is to deactivate the vault's ability to offer flash loans.

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

```
certoraRun contracts/unstoppable/FirstChallenge.conf
```

## Results

[Certora Results](https://prover.certora.com/output/1512/1b14f7e64fd841cdba46e160a5c418ab?anonymousKey=12bee694f43bafa5df07abcb788fa65cb9d68130)

The analysis reveals that the attacker can directly send DVT tokens to the lender contract (or use transferFrom), causing the `balanceBefore` assertion to consistently fail due to the `poolBalance` variable not being updated. This exploit renders flash loans unusable.

[Certora Results On Fix Version](https://prover.certora.com/output/1512/a5ba2f7458d5420aac760d61aac1f2db?anonymousKey=4bfd373d9e1ba1dca2e5a2d44a637e66bf0cc3ae)