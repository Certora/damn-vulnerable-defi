using UnstoppableLender as lender;
using DamnValuableToken as token;

methods{
    function _.receiveTokens(address tokenAddress, uint256 amount) external => DISPATCHER(true);
    function _.transfer(address, uint256) external => DISPATCHER(true);
    function token.totalSupply() external returns (uint256) envfree;
}

/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Find and show a path for each method.                                                                               │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/
rule reachability(method f)
{
	env e;
	calldataarg args;
	f(e,args);
	satisfy true;
}


/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ totalSupplyIsSumOfBalances                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/ 

persistent ghost mathint sum_of_balances {
    init_state axiom sum_of_balances == 0;
}

hook Sstore token._balances[KEY address a] uint new_value (uint old_value) {
    // when balance changes, update ghost
    sum_of_balances = sum_of_balances + new_value - old_value;
}

// This `sload` makes `sum_of_balances >= to_mathint(balance)` hold at the beginning of each rule.
hook Sload uint256 balance token._balances[KEY address a] {
  require sum_of_balances >= to_mathint(balance);
}

//// ## Part 4: Invariants

/** `totalSupply()` returns the sum of `balanceOf(u)` over all users `u`. */
invariant totalSupplyIsSumOfBalances()
    to_mathint(token.totalSupply()) == sum_of_balances;



/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ FlashLoan Denial of service                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/

// will give violation which show the attacker action that cause the flashloan to revert.
rule flashLoadDenialOfService()
{
    requireInvariant totalSupplyIsSumOfBalances();
    // Show it's possible for someUser to take out a flash loan
    env e1;
    require e1.msg.sender != currentContract && e1.msg.sender != lender && e1.msg.sender != token;

    uint256 amount;

    storage init = lastStorage;

    executeFlashLoan(e1, amount);

    // show that attacker could front run and cause the flashloan to revert
    env e2;
    require e1.msg.sender != e2.msg.sender && e2.msg.sender != currentContract && e2.msg.sender != lender && e2.msg.sender != token;

    method f;
    calldataarg args;

    f(e2, args) at init;

    // show the previously succeed flashloan reverts now
    executeFlashLoan@withrevert(e1, amount);
    assert !lastReverted;
}