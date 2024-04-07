/*
Solution to the challenge:
A user can request a flashloan from the pool with amount of 1000 (all the eth in the pool).
During the flashloan the user can deposit the eth taken back to the pool.
The pool will register all the eth on the user balance, however after the action is taken the pool 
only checks that it has at least the same balance as it did before (which holds since the user deposited
the eth).
The user can then freely withdraw the funds since the pool registered them on him.
*/

methods {
    function flashLoan(uint256) external;
    function _.execute() external => HAVOC_ALL;
}

rule flashLoanIntegrity {
    env e;
    uint256 amount;

    uint256 senderBalanceBefore = currentContract.balances[e.msg.sender];

    flashLoan(e, amount);
    
    assert currentContract.balances[e.msg.sender] == senderBalanceBefore;
}