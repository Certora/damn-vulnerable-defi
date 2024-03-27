methods {
    function _.receiveEther(uint256) external => DISPATCHER(true);
}


rule noChangeToOtherUser {
    method f;
    calldataarg args;
    env e;
    address someUser;

    uint256 someUserBalanceBefore = nativeBalances[someUser];
    
    f(e, args);
    
    assert someUserBalanceBefore != nativeBalances[someUser] => 
           someUser == e.msg.sender || someUser == f.contract;
}
