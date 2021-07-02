# NetSwap: NetObjex's Decentralized Exchange on Algorand
## Introduction
NetSwap is an Automated Market Maker (AMM) type decentralized exchange hosted on the Algorand blockchain.  
## NetSwap protocol
There are three participants in Netswap - Liquidity Providers (or LP), Traders (or users), and Protocol Developers (that's us). \
 \
- The Protocol developers are responsible for maintaining and upgrading the protocol. They also manage the creation of new Liquidity pools in the DEX. \
- Liquidity Providers deposit their funds in the Liquidity pools and in return receive a share of the trade fees generated during swapping. Since it is a single-sided liquidity protocol, liquidity providers can deposit either one of the pool tokens. At any time, they can withdraw their contribution to the pools using their LP tokens. \
- Traders can swap their tokens for another token from the liquidity pool. Each swap will be charged with a swap fee and a developer fee. 

## Pre-requisites
- python 3
- pyteal 0.7.0

## Instructions
Follow these instructions to deploy and test the DEX application. Also, create an environment file to declare values of the env variables. 

### Deploy contracts
Running the python code would compile and generate the smart contracts in TEAL.
```
cd contracts
python3 state_manager0.py
python3 state_manager1.py
python3 txn_verifier.py
python3 pool_escrow.py
python3 developer_lsig.py
```
Deploy each stateful TEAL contract in the order specified above, this will return an Application Index or AppID. \
Before deploying the current contract check whether it has a dependency on the App Index (or Indices) of a preceding contract and update it accordingly.

### Creating Liquidity Pool
To create a new liquidity pool, the developer has to configure a new escrow account to manage the funds. Create the Algorand assets (ASAs) required for the main tokens and LP tokens. Replace the TOKEN IDs accordingly in pool_escrow.py and developer_lsig.py. 
Compile the pool_escrow code to receive an escrow address and logic signature. Fund the escrow contract with required ALGOs and opt-in to stateful contracts.
Compile the developer_lsig code to receive the developer's lsig, to be used for minting tokens.

### Adding Liquidity
#### Type-1 Single Sided liquidity (TOKEN-1 contribution) :
The transaction to add single-sided liquidity to a pool is a group transaction containing five transactions. 
1. Call to txn_verifier stateful contract
2. Call to state_manager0 stateful contract
3. Asset transfer txn to add TOKEN-1 tokens to escrow from LP
4. Asset transfer txn to mint TOKEN-2 tokens to escrow by the protocol
5. Call to state_manager1 stateful contract to update state

The transaction to withdraw the unused TOKEN-1, TOKEN-2 tokens or to collect LP tokens is a group transaction containing three transactions. 
1. Call to txn_verifier stateful contract
2. Call to state_manager0 stateful contract
3. Asset transfer txn to withdraw TOKEN-1 or TOKEN-2 or LP tokens from escrow 

```
python3 type1_single_side_liq.py
```

#### Type-2 Single Sided liquidity (TOKEN-2 contribution) :
The transaction to add single-sided liquidity to a pool is a group transaction containing five transactions. 
1. Call to txn_verifier stateful contract
2. Call to state_manager0 stateful contract
3. Asset transfer txn to add TOKEN-2 tokens to escrow from LP
4. Asset transfer txn to burn protocol minted TOKEN-2 tokens from escrow 
5. Call to state_manager1 stateful contract to update state

The transaction to withdraw the unused TOKEN-2 tokens or to collect LP tokens is a group transaction containing three transactions. 
1. Call to txn_verifier stateful contract
2. Call to state_manager0 stateful contract
3. Asset transfer txn to withdraw TOKEN-2 or LP tokens from escrow to LP 

```
python3 type2_single_side_liq.py
```

### Token Swapping
The user must initially opt-in to the stateful contracts and assets involved before swapping.  

#### Swap TOKEN-1 for TOKEN-2 tokens (and vice-versa):
The transaction to swap tokens for another is a group transaction containing four transactions. 
1. Call to txn_verifier stateful contract
2. Call to state_manager1 stateful contract
3. Asset transfer txn to add TOKEN-1 or TOKEN-2 tokens to escrow from user
4. Call to state_manager0 stateful contract to update state

The transaction to withdraw the TOKEN-1 or TOKEN-2 tokens in exchange is a group transaction containing three transactions. 
1. Call to txn_verifier stateful contract
2. Call to state_manager1 stateful contract
3. Asset transfer txn to withdraw TOKEN-1 or TOKEN-2 tokens from escrow to the user

```
python3 swap_t1_for_t2.py
python3 swap_t2_for_t1.py
```
