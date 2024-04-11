# Challenge 2 - Side Entrance
A surprisingly simple pool allows anyone to deposit ETH, and withdraw it at any point in time.

It has 1000 ETH in balance already, and is offering free flash loans using the deposited ETH to promote their system.

Starting with 1 ETH in balance, pass the challenge by taking all ETH from the pool.


### Finding The Bug
We want to check that the pool is solvent, that means that the amount of ETH the pool has have to be at least the amount of the sum of balances the users deposited to the pool.

Let's run this invariant using: 
```certoraRun contracts/side-entrance/Challenge4.conf```

[A report of that run](https://prover.certora.com/output/15800/5da8b876b52c44f4a8cd9b59b9eeca3c?anonymousKey=26d1ee5b21c5d19dbb1dfe83a260bebed15ad396)

If you'll inspect the spec we wrote you'll notice that we summarized the execute function to call the deposit function of the pool. This is an under approximation since the execute function can actually do anything but the attack vector is through interaction with the pool during a flash loan.
We can see that the invariant failed for the flashLoan function but also for withdraw. As a bonus our prover found that the sendValue method that withdraw uses can call anything (it havocs) and is vulnerable to reentrancy. This is out of the scope of the challenge though and that is the reason we excluded the withdraw function from the execute summarization.

Focusing on the case where a user called the deposit function of the pool during a flash loan, we can see that it made the pool insolvent as that user was able to increase his balance in the contract with the funds he flash loaned and fool the contract that flash loan was paid back without actually paying it back.
A user that exploited this case while asking for the entire ETH balance of the pool can after the flashloan call the withdraw function to empty the pool.

### Fixing The Bug
To fix this bug we added an internal accounting mechanism to the pool. This internalAccounting field will keep track of the balance of ETH the pool should have and will increase with new deposits and decrease with withdraws by the appropriate amount. We modified the require at the end of the flashLoan function to now check that the difference between the actual balance of the pool and the internalAccounting does not shrink after a flashloan. This effectively blocks anyone from depositing ETH they flashloaned from the pool, making the pool solvent.

To run the fixed version:
```certoraRun contracts/naive-receiver/Challenge2Fixed.conf```

[A report of that run](https://prover.certora.com/output/15800/eb0ab86a3006459f81abd827b682d82b?anonymousKey=3125d856b4ae90fbe98d8821a450d0cb6c51e2b2)

Even though our pool is solvent now the invariant will still fail for the withdraw function as it is vulnerable like explained above.