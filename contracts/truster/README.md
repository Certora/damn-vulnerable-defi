# Third Challenge

## Challenge #3 - Truster

In this challenge, a new pool has launched that is offering flash loans of DVT tokens for free. 
To pass this challenge, take all tokens out of the pool. If possible, in a single transaction.

### 1. Contracts

- `contracts/truster/TrusterLenderPool.sol`
- `contracts/DamnValuableToken.sol`

### 2. Specification

- `contracts/truster/TrusterLenderPool.spec`

#### Example Specifications:

- **poolAllowanceAlwaysZero**: Makes sure that the pool's allowance is always zero.

## Execution

```
certoraRun contracts/truster/truster.conf
```

## Results

[Certora Results](https://prover.certora.com/output/1512/0c3d914076c84171b3020e7d265f246e?anonymousKey=c4583821b1bbca38529b1dd5e00fd75ce412161b)

The analysis reveals that the flash loan function can be used to give any user any amount of allowance from the contract which potentially can be used later to drain the pool.

In order to fix that bug the pool creator should add limitation on the usage of the following: 
``` 
(bool success, ) = target.call(data);
```
Which allows the poll contract to be a msg.sender of **Any Call!!!** 


## Fix

The fix involve enforce the target to implement predefine interface function which prevents the lender contract to be used as msg.sender to the approve function.

### Contracts

- `contracts/truster/FixedTrusterLenderPool.sol`
- `contracts/truster/ReceiverDummy.sol`
- `contracts/DamnValuableToken.sol`

### Spec
- `contracts/truster/TrusterLenderPool.spec`

### Execution

```
certoraRun contracts/truster/FixedTruster.conf
```

### Results
[Certora Results](https://prover.certora.com/output/1512/c0b089254623435e80216483437582f2?anonymousKey=09697121eafc49bf34b390436ea8014ac0e1b5b6)