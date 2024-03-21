
using DamnValuableToken as token;
using FlashLoanAttacker as attacker;

methods{
    function token.totalSupply() external returns (uint256) envfree;
     function _._ external => DISPATCH [
        token.approve(address,uint256)
    ] default HAVOC_ALL;
}


/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Rules: Find and show a path for each method.                                                                        │
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
│ Invariant: totalSupply is the sum of all balances                                                                   │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/
persistent ghost mathint sumOfBalances {
    init_state axiom sumOfBalances == 0;
}

hook Sload uint256 balance token._balances[KEY address addr] {
    require sumOfBalances >= to_mathint(balance);
}

hook Sstore token._balances[KEY address addr] uint256 newValue (uint256 oldValue) {
    sumOfBalances = sumOfBalances - oldValue + newValue;
}

invariant totalSupplyIsSumOfBalances()
    to_mathint(token.totalSupply()) == sumOfBalances;
`
/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Pool Balance Cant Decrease                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/

rule poolBalanceCantDecrease(){
    env e;
    method f;
    calldataarg args;

    requireInvariant totalSupplyIsSumOfBalances();
    require e.msg.sender != currentContract && e.msg.sender != attacker;
    require token.allowance(e, currentContract, e.msg.sender) == 0;
    
    uint256 poolBalanceBefore = token.balanceOf(e, currentContract);

    f(e, args);

    uint256 poolBalanceAfter = token.balanceOf(e, currentContract);

    assert poolBalanceBefore <= poolBalanceAfter;
}