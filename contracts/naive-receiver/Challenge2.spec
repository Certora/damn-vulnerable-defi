methods {
    function flashLoan(address, uint256) external envfree;
    function fixedFee() external returns(uint256) envfree;
}

rule flashLoanIntegrity {
    address burrower;
    uint256 burrowAmount;

    balanceBefore = nativeBalances[currentContract];
    flashLoan(burrower, burrowAmount);
    balanceAfter = nativeBalances[currentContract];

    assert balanceAfter == balanceBefore + fixedFee();
}