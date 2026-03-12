import hre from "hardhat";

async function main() {

  const Registry = await hre.ethers.getContractFactory("ModelRegistry");

  const registry = await Registry.deploy();

  await registry.waitForDeployment();

  const address = await registry.getAddress();

  console.log("ModelRegistry deployed to:", address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});