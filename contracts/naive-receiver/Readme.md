# Challenge 2 - Naive Receiver
There’s a pool with 1000 ETH in balance, offering flash loans. It has a fixed fee of 1 ETH.
A user has deployed a contract with 10 ETH in balance. It’s capable of interacting with the pool and receiving flash loans of ETH.
Take all ETH out of the user’s contract. If possible, in a single transaction.

### Finding The Bug
Using the prover we wrote a parametric rule `noChangeToOtherUser` that checks that no interaction with the pool can result in
the balance of some other user to change. An address that calls a function of the pool should only be able to affect the balances of itself and the pool contract.

Let's run this rule using: 
```certoraRun contracts/naive-receiver/Challenge2.conf```

[A report of that run](https://prover.certora.com/output/15800/45273ead5ad849e4957246d26d7f1d35?anonymousKey=0e49806ed54a6b6f2e4b462ce84c1d6371d4a2d8)

We can see that the rule failed. Inspecting the call trace we can see that's something is wrong here, a random user was able to call the `flashLoan` function for our FlashLoanReceiver without any permission or allowance. This is the bug, because any user can ask for a flashLoan for a random borrower he can actually keep calling the flashLoan function as many times as he wants, and every time the borrower would have to pay the fee even though he didn't not asked to borrower.

### Fixing The Bug
To fix the bug we removed the borrower parameter from the `flashLoan` function of the pool. Instead the function is using the message sender as the borrower and every borrower will have to ask for a flash flash for himself.

To run the fixed version:
```certoraRun contracts/naive-receiver/Challenge2Fixed.conf```

[A report of that run](ttps://prover.certora.com/output/15800/fba8a090368d49c2bf3542fc9d885939?anonymousKey=77a4776fce13812ff376d2f681fde5ec97cdab70)