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
certoraRun contracts/unstoppable/FirstChallenge.conf --server staging --prover_version master
```

## Results

[Certora Results](https://prover.certora.com/output/1512/478297d78de540edb46b7fa18dcdc81f?anonymousKey=a61c4eeedb2ab7e1deb6d684c35baafa8cb56cd1)

The analysis reveals that the attacker can directly send DVT tokens to the lender contract, causing the `balanceBefore` assertion to consistently fail due to the `poolBalance` variable not being updated. This exploit renders flash loans unusable.