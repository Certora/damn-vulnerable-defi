using FlashLoanReceiver as Receiver;
using NaiveReceiverLenderPool as Pool;

methods {
    //function flashLoan(address, uint256) external envfree;
    //function fixedFee() external returns(uint256) envfree;
    function _.receiveEther(uint256) external => DISPATCHER(true);
    function _.flashLoan(address, uint256) external => DISPATCHER(true);
    function attack(address, address) external envfree;
}

rule attacking {
    attack(Pool, Receiver);
    assert nativeBalances[Receiver] == 0;
}

/*
rule userBalanceDecreseByFeeAmount {
    address borrower;
    uint256 borrowAmount;

    uint256 balanceBefore = nativeBalances[Receiver];
    flashLoan(borrower, borrowAmount);
    uint256 balanceAfter = nativeBalances[Receiver];

    assert to_mathint(balanceBefore) >= balanceAfter - fixedFee();

}


rule flashLoanIntegrity {
    address borrower;
    uint256 borrowAmount;

    uint256 balanceBefore = nativeBalances[currentContract];
    flashLoan(borrower, borrowAmount);
    uint256 balanceAfter = nativeBalances[currentContract];

    assert to_mathint(balanceAfter) == balanceBefore + fixedFee();
}
*/