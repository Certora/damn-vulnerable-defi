pragma solidity ^0.8.20;

import "@openzeppelin/contracts/utils/Address.sol";

interface IFlashLoanEtherReceiver {
    function execute() external payable;
}

contract SideEntranceLenderPool {
    using Address for address payable;

    mapping (address => uint256) private balances;

    uint256 internalAccounting;

    constructor() public payable {
        internalAccounting = msg.value;
    }

    function deposit() external payable {
        balances[msg.sender] += msg.value;
        internalAccounting += msg.value;
    }

    function withdraw() external {
        uint256 amountToWithdraw = balances[msg.sender];
        balances[msg.sender] = 0;
        payable(msg.sender).sendValue(amountToWithdraw);
        internalAccounting -= amountToWithdraw;
    }

    function flashLoan(uint256 amount) external {
        uint256 balanceBefore = address(this).balance;
        uint256 differenceBefore = address(this).balance - internalAccounting;
        require(balanceBefore >= amount, "Not enough ETH in balance");

        IFlashLoanEtherReceiver(msg.sender).execute{value: amount}();

        require(address(this).balance - internalAccounting >= differenceBefore, "Flash loan hasn't been paid back");        
    }
}
 