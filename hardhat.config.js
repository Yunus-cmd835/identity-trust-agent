require("@nomiclabs/hardhat-ethers");
require("dotenv").config();

module.exports = {
  defaultNetwork: "sepolia",
  networks: {
    sepolia: {
      url: process.env.SEPOLIA_RPC_URL,
      accounts: [process.env.PRIVATE_KEY],
    },
  },
  solidity: "0.8.19",
};
