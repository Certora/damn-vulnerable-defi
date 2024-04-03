using FlashLoanerPool as flashloan;

/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ DepositFunction cant be used by flashloan                                                                           │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/
rule DepositCantBeInvokedByFlashLoan()
{
	env e;
    require e.msg.sender == flashloan && isContract(e, e.msg.sender);

    uint256 amount;

    deposit@withrevert(e, amount);

    assert lastReverted;
}