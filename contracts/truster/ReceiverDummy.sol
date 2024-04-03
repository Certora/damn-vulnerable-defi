pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract ReceiverDummy{
    
    function execute(bytes memory data) external returns (bool, uint) {
        return (true, 0);
    }
}