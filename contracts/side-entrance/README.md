# Challenge 2 - Side Entrance
A surprisingly simple pool allows anyone to deposit ETH, and withdraw it at any point in time.

It has 1000 ETH in balance already, and is offering free flash loans using the deposited ETH to promote their system.

Starting with 1 ETH in balance, pass the challenge by taking all ETH from the pool.


### Finding The Bug
We want to check that the pool is solvent. That means that the amount of ETH the pool holds has to be at least the sum of the balances the users deposited to the pool.

Let's run this invariant using: 
```certoraRun contracts/side-entrance/Challenge4.conf```

[A report of that run](https://prover.certora.com/output/15800/09103d29281f49ea99460371b3d650bc?anonymousKey=3e347321ecdd4c22b3a704c50ce10e770d7884c4)

If you'll inspect the spec we wrote you'll notice that we summarized the execute function to simulate the different functions of the pool. This is an under approximation since the execute function can actually do anything but the attack vector is through interaction with the pool during a flash loan.
The invariant failed for the flashLoan function while calling back the withdraw function. We can see that a user was able to make the pool insolvent by increasing his balance in the contract with the funds he flash loaned and fooling the contract that flash loan was paid back without actually paying it back.
A user that exploited this case while asking for the entire ETH balance of the pool can after the flashloan call the withdraw function to empty the pool.

### Fixing The Bug
To fix this bug we added an internal accounting mechanism to the pool. This internalAccounting field will keep track of the balance of ETH the pool should have and will increase with new deposits and decrease with withdraws by the appropriate amount. We modified the require at the end of the flashLoan function to now check that the difference between the actual balance of the pool and the internalAccounting does not shrink after a flashloan. This effectively blocks anyone from depositing ETH they flashloaned from the pool, making the pool solvent.

To run the fixed version:
```certoraRun contracts/naive-receiver/Challenge2Fixed.conf```

[A report of that run](https://prover.certora.com/output/15800/f25ef1a5f19b499c9cb9d7f7f65bbe50?anonymousKey=058f7081eefd92e14ad16f33139f91318a95c814)
