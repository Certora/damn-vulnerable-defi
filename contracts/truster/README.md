# Third Challenge

## Challenge #3 - Truster

In this challenge, a new pool has launched that is offering flash loans of DVT tokens for free. 
To pass this challenge, take all tokens out of the pool. If possible, in a single transaction.

### 1. Contracts

- `contracts/truster/TrusterLenderPool.sol`
- `contracts/truster/FlashLoanAttacker.sol`
- `contracts/DamnValuableToken.sol`

### 2. Specification

- `contracts/truster/TrusterLenderPool.spec`

#### Example Specifications:

- **poolBalanceCantDecrease**: Makes sure that the pool's balance cannot decrease.

## Execution

```
certoraRun contracts/truster/truster.conf
```

## Results

[Certora Results](https://prover.certora.com/output/1512/98a051e83c80468f8bbec22f051eeab8?anonymousKey=714355c70013e4acf94ddb8946dca59b6b790ff2)

The analysis reveals that the attacker can create a contract that calls the flashLoan and pass to it the approve signature with the arguments of the msg.sender and the pool's balance, which will be called by the targeted pool contract. after that the contract will call transferFrom function which will send all the pool balance to the attacker.

In order to fix that bug the pool creator should add limitation on the usage of the following: 
```
(bool success, ) = target.call(data);
```
Which allows the poll contract to be a msg.sender of **Any Call!!!** 