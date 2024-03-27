
using DamnValuableToken as token;

methods{
    function token.totalSupply() external returns (uint256) envfree;
    function token.allowance(address, address) external returns (uint256) envfree;
    function _.execute(bytes) external => DISPATCHER(true);
    function _._ external => DISPATCH [
        token._, 
        currentContract._
    ] default NONDET;
}

/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Pool Allowance Always Zero                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/

invariant poolAllowanceAlwaysZero(address user)
    token.allowance(currentContract, user) == 0
    {
        preserved with (env e)
        {
            require e.msg.sender != currentContract;
        } 
    }