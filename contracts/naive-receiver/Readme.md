# Challenge 2 - Naive Receiver
There’s a pool with 1000 ETH in balance, offering flash loans. It has a fixed fee of 1 ETH.
A user has deployed a contract with 10 ETH in balance. It’s capable of interacting with the pool and receiving flash loans of ETH.
Take all ETH out of the user’s contract. If possible, in a single transaction.

### Finding The Bug
Using the prover we wrote a parametric rule `noChangeToOtherUser` that checks that no interaction with the pool can result in
the balance of some other user to change. An address that calls a function of the pool should only be able to affect the balances of itself and the pool contract.

Let's run this rule using: 
```certoraRun contracts/naive-receiver/Challenge2.conf```

[A report of that run](https://prover.certora.com/output/15800/2c9332ff3482449cb85e00e6ac696934?anonymousKey=7a22a08b20334987a38f73c493f84775d12ee52a)

We can see that the rule failed. Inspecting the call trace we can see that's something is wrong here, a random user was able to call the `flashLoan` function for our FlashLoanReceiver without any permission or allowance. This is the bug, because any user can ask for a flashLoan for a random borrower he can actually keep calling the flashLoan function as many times as he wants, and every time the borrower would have to pay the fee even though he didn't not asked to borrower.

### Fixing The Bug
To fix the bug we removed the borrower parameter from the `flashLoan` function of the pool. Instead the function is using the message sender as the borrower and every borrower will have to ask for a flash flash for himself.

To run the fixed version:
```certoraRun contracts/naive-receiver/Challenge2Fixed.conf```

[A report of that run](https://prover.certora.com/output/15800/dae10f305c904a83a725bb8de0b480c7?anonymousKey=907f5e1f126037620f3f7c263ef9af8f233f6b00)