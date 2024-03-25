methods {
    function _.receiveEther(uint256) external => DISPATCHER(true);
}

/*
rule flashLoanDoesNotChangeThirdParty {
    env e;
    address borrower;
    uint256 amount;
    address otherUser;

    uint256 otherUserBalanceBefore = nativeBalances[otherUser];
    flashLoan(borrower, amount);

    assert nativeBalances[otherUser] != otherUserBalanceBefore => otherUser == e.msg.sender;
}
*/

rule noChangeToOtherUser(method f) filtered { f -> f.contract == currentContract } {
    env e;
    calldataarg args;
    address someUser;

    uint256 someUserBalanceBefore = nativeBalances[someUser];
    
    f(e, args);
    
    assert someUserBalanceBefore != nativeBalances[someUser] => 
           someUser == e.msg.sender || someUser == currentContract;
}
