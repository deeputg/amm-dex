# NetSwap : NetObjex Decentralized Exchange on Algorand Blockchain
## Introduction
NetSwap is an AMM decentralized exchange on Algorand blockchain.
## Netswap protocol
There are three participants in Netswap - Liquidity providers(LP), Traders(users), Protocol Developers - of the DEX dApp create three deferent transaction types. The Protocol developer creates a Liquidity pool by deploying the escrow contract. Liquidity Providers deposites funds to the already created Liquidity pools. Since it is a single sided liquidity protocol, liquidity providers can deposite eaither one of the pool tokens. Traders choose and swap there token from the liquidity pool. Each swap will be charged with a swap fee of 0.45% and protocol developer fee of 0.05%. The Liequidity providers can withdrow there funds from the pools using the lp tokens.


## Pre requisits
- python 3
- pyteal 0.7.0

## Instructions
Please follow the following instructions to deploy and test the dex application.

### pyteal to teal
```
cd contracts
python3 state_manager0.py
python3 state_manager1.py
python3 txn_verifier.py
python3 pool_excrow.py
python3 developer_lsig.py
cd ..
```

### Creating Liquidity Pool

### Adding Liquidity

### Swapping

