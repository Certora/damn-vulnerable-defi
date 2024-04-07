# Challenge 2 - Side Entrance
A surprisingly simple pool allows anyone to deposit ETH, and withdraw it at any point in time.

It has 1000 ETH in balance already, and is offering free flash loans using the deposited ETH to promote their system.

Starting with 1 ETH in balance, pass the challenge by taking all ETH from the pool.


### Finding The Bug
We wanted to check the integrity of the `flashLoan` function, that is, to see that the user cannot affect he's balance at the pool while taking a flash loan. 

Let's run this rule using: 
```certoraRun contracts/side-entrance/Challenge4.conf```

[A report of that run](https://prover.certora.com/output/15800/b1b578757348453e93910e382ef0cb92?anonymousKey=cb376b173b4278daeb03b66bb6e0a7fc542c335c)

We can see that the rule failed. The user was able to affect his balance on the pool. This is risky because, if the user is able to change his balance using the flash loan he took, he could fool the contract into thinking the loan was payed and then withdraw all of his balance.

### Fixing The Bug
To fix the bug we modify the require ate the end of the `flashLoan` function to assert the the user can't affected his balance during the flash loan.

To run the fixed version:
```certoraRun contracts/naive-receiver/Challenge2Fixed.conf```

[A report of that run](https://prover.certora.com/output/15800/e5bea4aa88644ddbab07db6539ab9feb?anonymousKey=f0b7c6fe621090630e0a1beaf0dbeb6cdd5f426b)