from pyteal import *

KEY_TOTAL_TOKEN1_BAL = Bytes("B1")
KEY_TOTAL_TOKEN2_BAL = Bytes("B2")
KEY_TOTAL_SS1_LP_TOKEN_DIST = Bytes("LD1")
KEY_TOTAL_SS2_LP_TOKEN_DIST = Bytes("LD2")
KEY_TOTAL_TOKEN2_MINTED_BAL = Bytes("B2M")
KEY_TOTAL_TOKEN2_TO_BURN = Bytes("BURN")
KEY_PROTOCOL_UNUSED_SS1_LP = Bytes("P1")

KEY_TOKEN1 = Bytes("T1")
KEY_TOKEN2 = Bytes("T2")
KEY_SS1_LP_TOKEN = Bytes("SSLT")
KEY_SS2_LP_TOKEN = Bytes("SSLT2")

KEY_USER_UNUSED_TOKEN1 = Bytes("U1")
KEY_USER_UNUSED_TOKEN2 = Bytes("U2")
KEY_USER_UNUSED_SS1_LP = Bytes("S1")
KEY_USER_UNUSED_SS2_LP = Bytes("S2")

TXN_TYPE_SWAP_DEPOSIT_TOKEN1_TO_TOKEN2 = Bytes("s1")
TXN_TYPE_SWAP_DEPOSIT_TOKEN2_TO_TOKEN1 = Bytes("s2")
TXN_TYPE_ADD_T1_SINGLE_LP_DEPOSIT = Bytes("a")
TXN_TYPE_ADD_T2_SINGLE_LP_DEPOSIT = Bytes("b")
TXN_TYPE_REFUND = Bytes("r")
TXN_TYPE_PROTOCOL_REFUND = Bytes("p")

def approval_program():
    
    # Read from additional account
    read_key_token1 = App.localGet(Int(1), KEY_TOKEN1)
    read_key_token2 = App.localGet(Int(1), KEY_TOKEN2)
    read_key_ss1_lp_token = App.localGet(Int(1), KEY_SS1_LP_TOKEN)
    read_key_ss2_lp_token = App.localGet(Int(1), KEY_SS2_LP_TOKEN)

    read_key_total_token1_bal = App.localGet(Int(1), KEY_TOTAL_TOKEN1_BAL)
    read_key_total_token2_bal = App.localGet(Int(1), KEY_TOTAL_TOKEN2_BAL)
    read_key_total_ss1_lp_token_dist = App.localGet(Int(1), KEY_TOTAL_SS1_LP_TOKEN_DIST)
    read_key_total_ss2_lp_token_dist = App.localGet(Int(1), KEY_TOTAL_SS2_LP_TOKEN_DIST)
    read_key_total_token2_minted_bal = App.localGet(Int(1), KEY_TOTAL_TOKEN2_MINTED_BAL)
    read_protocol_unused_token2 = App.localGet(Int(1), KEY_TOTAL_TOKEN2_TO_BURN)
    read_protocol_unused_ss1_lp = App.localGet(Int(1), KEY_PROTOCOL_UNUSED_SS1_LP)

    # Write to additional account
    def write_key_total_token1_bal(bal: Int): return App.localPut(Int(1), KEY_TOTAL_TOKEN1_BAL, bal)
    def write_key_total_token2_bal(bal: Int): return App.localPut(Int(1), KEY_TOTAL_TOKEN2_BAL, bal)
    def write_key_total_token2_minted_bal(bal: Int): return App.localPut(Int(1), KEY_TOTAL_TOKEN2_MINTED_BAL, bal)
    def write_key_total_ss1_lp_token_dist(bal: Int): return App.localPut(Int(1), KEY_TOTAL_SS1_LP_TOKEN_DIST, bal)
    def write_key_total_ss2_lp_token_dist(bal: Int): return App.localPut(Int(1), KEY_TOTAL_SS2_LP_TOKEN_DIST, bal)
    def write_protocol_unused_token2(bal: Int): return App.localPut(Int(1), KEY_TOTAL_TOKEN2_TO_BURN, bal)
    def write_protocol_unused_ss1_lp(bal: Int): return App.localPut(Int(1), KEY_PROTOCOL_UNUSED_SS1_LP, bal)

    # Read from sender account
    def read_user_unused_token1(address: Bytes): return App.localGet(Int(0), Concat(KEY_USER_UNUSED_TOKEN1, address))
    def read_user_unused_token2(address: Bytes): return App.localGet(Int(0), Concat(KEY_USER_UNUSED_TOKEN2, address))
    def read_user_unused_ss1_lp(address: Bytes): return App.localGet(Int(0), Concat(KEY_USER_UNUSED_SS1_LP, address))
    def read_user_unused_ss2_lp(address: Bytes): return App.localGet(Int(0), Concat(KEY_USER_UNUSED_SS2_LP, address))
    
    
    # Write to sender account
    def write_user_unused_token1(address: Bytes, amount: Int): return App.localPut(Int(0), Concat(KEY_USER_UNUSED_TOKEN1, address), amount)
    def write_user_unused_token2(address: Bytes, amount: Int): return App.localPut(Int(0), Concat(KEY_USER_UNUSED_TOKEN2, address), amount)
    def write_user_unused_ss1_lp(address: Bytes, amount: Int): return App.localPut(Int(0), Concat(KEY_USER_UNUSED_SS1_LP, address), amount)
    def write_user_unused_ss2_lp(address: Bytes, amount: Int): return App.localPut(Int(0), Concat(KEY_USER_UNUSED_SS2_LP, address), amount)

    # Scratch Vars
    scratchvar_token1_used = ScratchVar(TealType.uint64)
    scratchvar_token2_used = ScratchVar(TealType.uint64)
    scratchvar_total_token1_bal = ScratchVar(TealType.uint64)
    scratchvar_total_token2_bal = ScratchVar(TealType.uint64)
    scratchvar_total_ss1_lp_token_dist = ScratchVar(TealType.uint64)
    scratchvar_total_ss2_lp_token_dist = ScratchVar(TealType.uint64)
    scratchvar_new_liquidity = ScratchVar(TealType.uint64)
    scratchvar_temp = ScratchVar(TealType.uint64)
    scratchvar_temp_token2_used = ScratchVar(TealType.uint64)
    scratchvar_total_token2_minted_bal = ScratchVar(TealType.uint64)
    scratchvar_total_token2_burn_bal = ScratchVar(TealType.uint64)
    scratchvar_protocol_unused_ss1 = ScratchVar(TealType.uint64)

    #Read from Additional account of STATE MANAGER1 contract
    key_token1_other = App.localGetEx(Int(1), Btoi(Txn.application_args[2]), KEY_TOTAL_TOKEN1_BAL)
    key_token2_other = App.localGetEx(Int(1), Btoi(Txn.application_args[2]), KEY_TOTAL_TOKEN2_BAL)
    
    on_create = Int(1) 

    on_closeout = Int(1)

    on_opt_in = If(Txn.application_args.length() == Int(4), 
        Seq([
            App.localPut(Int(0), KEY_TOKEN1, Btoi(Txn.application_args[0])),
            App.localPut(Int(0), KEY_TOKEN2, Btoi(Txn.application_args[1])),
            App.localPut(Int(0), KEY_SS1_LP_TOKEN, Btoi(Txn.application_args[2])),
            App.localPut(Int(0), KEY_SS2_LP_TOKEN, Btoi(Txn.application_args[3])),
            Int(1),
        ]),
        Int(1)
    )

    on_add_single_t1_lp_deposit = Seq([
        scratchvar_total_token1_bal.store(read_key_total_token1_bal),
        scratchvar_total_token2_bal.store(read_key_total_token2_bal),
        scratchvar_total_token2_minted_bal.store(read_key_total_token2_minted_bal),
        scratchvar_total_ss1_lp_token_dist.store(read_key_total_ss1_lp_token_dist),
        scratchvar_total_ss2_lp_token_dist.store(read_key_total_ss2_lp_token_dist),
        scratchvar_total_token2_burn_bal.store(read_protocol_unused_token2),
        scratchvar_protocol_unused_ss1.store(read_protocol_unused_ss1_lp),
        If(
            # If TOTAL_LIQUIDITY_TOKEN_DISTRIBUTED = 0
            scratchvar_total_ss1_lp_token_dist.load() + scratchvar_total_ss2_lp_token_dist.load() == Int(0),
                
            # Then, token1_used = token1_deposit
            # token2_used = token2_deposit
            # new_liquidity = token1_deposit
            Seq([
                scratchvar_token1_used.store(Gtxn[2].asset_amount()),
                scratchvar_token2_used.store(Gtxn[3].asset_amount()),
                scratchvar_new_liquidity.store(Gtxn[2].asset_amount()),
            ]),
            # Else, token1_used = min(token1_deposit, (token2_deposit * TOTAL_TOKEN1_BALANCE / TOTAL_TOKEN2_BALANCE))
            # token2_used = min(token2_deposit, token1_deposit * TOTAL_TOKEN2_BALANCE / TOTAL_TOKEN1_BALANCE)
            Seq([
                scratchvar_temp.store(Gtxn[3].asset_amount() * scratchvar_total_token1_bal.load() / scratchvar_total_token2_bal.load()),
                If(
                    # If token1_deposit is min
                    Gtxn[2].asset_amount() < scratchvar_temp.load(),
                    # token1_used = token1_deposit
                    scratchvar_token1_used.store(Gtxn[2].asset_amount()),
                    # Else, token1_used = (token2_deposit * TOTAL_TOKEN1_BALANCE / TOTAL_TOKEN2_BALANCE))
                    scratchvar_token1_used.store(scratchvar_temp.load()),
                ),
                scratchvar_temp.store(Gtxn[2].asset_amount() * scratchvar_total_token2_bal.load() / scratchvar_total_token1_bal.load()),
                If(
                    # If token2_deposit is min
                    Gtxn[3].asset_amount() < scratchvar_temp.load(),
                    # token2_used = token2_deposit
                    scratchvar_token2_used.store(Gtxn[3].asset_amount()),
                    # Else, token2_used = token1_deposit * TOTAL_TOKEN2_BALANCE / TOTAL_TOKEN1_BALANCE)
                    scratchvar_token2_used.store(scratchvar_temp.load()),
                ),
                scratchvar_new_liquidity.store(scratchvar_total_ss1_lp_token_dist.load() * 
                                                scratchvar_token1_used.load() / scratchvar_total_token1_bal.load()),
            ])
        ),
        # Assert new_liquidity >= min_liquidity_required_by_LP
        Assert(
            scratchvar_new_liquidity.load() >= Btoi(Txn.application_args[1]),
        ),
        
        # USER_UNUSED_TOKEN1 = USER_UNUSED_TOKEN1 + token1_deposit - token1_used
        write_user_unused_token1(
            Txn.accounts[1],
            read_user_unused_token1(Txn.accounts[1]) + Gtxn[2].asset_amount() - scratchvar_token1_used.load()
        ),
        # USER_UNUSED_TOKEN2 = USER_UNUSED_TOKEN2 + token2_deposit - token2_used
        write_protocol_unused_token2(
            scratchvar_total_token2_burn_bal.load() + Gtxn[3].asset_amount() - scratchvar_token2_used.load()
        ),
    
        # TOTAL_TOKEN1_BALANCE = TOTAL_TOKEN1_BALANCE + token1_used
        write_key_total_token1_bal(scratchvar_total_token1_bal.load() + scratchvar_token1_used.load()),

        # TOTAL_TOKEN2_BALANCE = TOTAL_TOKEN2_BALANCE + token2_used
        write_key_total_token2_bal(scratchvar_total_token2_bal.load() + scratchvar_token2_used.load()),

        # TOTAL_TOKEN2_MINTED_BALANCE = TOTAL_TOKEN2_MINTED_BALANCE + token2_used
        write_key_total_token2_minted_bal(scratchvar_total_token2_minted_bal.load() + scratchvar_token2_used.load()),

        # USER_UNUSED_LIQUIDITY = USER_UNUSED_LIQUIDITY + (total_liquidity * token1_deposit / TOTAL_TOKEN1_BALANCE)/2
        write_user_unused_ss1_lp(
            Txn.accounts[1],
            read_user_unused_ss1_lp(Txn.accounts[1]) + (scratchvar_new_liquidity.load()/Int(2))),

        # PROTOCOL_UNUSED_LIQUIDITY = PROTOCOL_UNUSED_LIQUIDITY + (total_liquidity * token1_deposit / TOTAL_TOKEN1_BALANCE)/2
        write_protocol_unused_ss1_lp(
            scratchvar_protocol_unused_ss1.load() + (scratchvar_new_liquidity.load()/Int(2))),    

        # TOTAL_LIQUIDITY_TOKEN_DISTRIBUTED += new_liquidity
        write_key_total_ss1_lp_token_dist(scratchvar_total_ss1_lp_token_dist.load() + scratchvar_new_liquidity.load()),
        Int(1)
    ])
    
    on_add_single_t2_lp_deposit = Seq([
        scratchvar_total_token2_bal.store(read_key_total_token2_bal),
        scratchvar_total_token2_minted_bal.store(read_key_total_token2_minted_bal),
        scratchvar_total_ss1_lp_token_dist.store(read_key_total_ss1_lp_token_dist),
        scratchvar_total_ss2_lp_token_dist.store(read_key_total_ss2_lp_token_dist),
        scratchvar_total_token2_burn_bal.store(read_protocol_unused_token2),
        scratchvar_protocol_unused_ss1.store(read_protocol_unused_ss1_lp),
        
        #TOKEN-1 liquidity should have been added prior to this 
        Assert(
            scratchvar_total_token2_minted_bal.load() > Int(0)
        ),
        
        #LP added TOKEN-2 = TOTAL_TOKEN2_BALANCE - TOTAL_TOKEN2_MINTED_BALANCE
        scratchvar_temp.store(scratchvar_total_token2_bal.load() - scratchvar_total_token2_minted_bal.load()), 
        
        #token2_used = min(token2_deposit, TOTAL_TOKEN2_MINTED_BALANCE)
        If(
            Gtxn[2].asset_amount() < scratchvar_total_token2_minted_bal.load(),
            scratchvar_temp_token2_used.store(Gtxn[2].asset_amount()),
            scratchvar_temp_token2_used.store(scratchvar_total_token2_minted_bal.load())
        ),

        #Check if First addition of TOKEN2 liquidity
        If(
            scratchvar_total_ss2_lp_token_dist.load() == Int(0),
            scratchvar_new_liquidity.store(scratchvar_temp_token2_used.load()),
            scratchvar_new_liquidity.store(scratchvar_total_ss2_lp_token_dist.load() * 
                                                      scratchvar_temp_token2_used.load() / scratchvar_temp.load())
        ),

        # Assert new_liquidity >= min_liquidity_required_by_LP
        Assert(
            scratchvar_new_liquidity.load() >= Btoi(Txn.application_args[1]),
        ),

        #USER_UNUSED_TOKEN2 = USER_UNUSED_TOKEN2 + token2_deposit - token2_used
        write_user_unused_token2(
            Txn.accounts[1], 
            read_user_unused_token2(Txn.accounts[1]) + (Gtxn[2].asset_amount() - scratchvar_temp_token2_used.load())
        ),
        
        #PROTOCOL_UNUSED_TOKEN2 = PROTOCOL_UNUSED_TOKEN2 + token2_used  (to be burned)
        write_protocol_unused_token2(
            scratchvar_total_token2_burn_bal.load() + scratchvar_temp_token2_used.load()
        ),

        #USER_UNUSED_SS2_LP = USER_UNUSED_SS2_LP + TOTAL_SS2_LIQUIDITY * (token2_used / total_user_added_token2) 
        write_user_unused_ss2_lp(
            Txn.accounts[1],
            read_user_unused_ss2_lp(Txn.accounts[1]) + (scratchvar_new_liquidity.load()/Int(2))
        ),
        
        #PROTOCOL_UNUSED_SS1_LP = PROTOCOL_UNUSED_SS1_LP - TOTAL_SS2_LIQUIDITY * (token2_used / total_user_added_token2) 
        write_protocol_unused_ss1_lp(
            scratchvar_protocol_unused_ss1.load() - (scratchvar_new_liquidity.load()/Int(2))),    

        #TOTAL_TOKEN2_MINTED_BALANCE = TOTAL_TOKEN2_MINTED_BALANCE - token2_used 
        write_key_total_token2_minted_bal(scratchvar_total_token2_minted_bal.load() -  scratchvar_temp_token2_used.load()),
        
        #TOTAL_SS2_LIQUIDITY_TOKENS = TOTAL_SS2_LIQUIDITY_TOKENS + new_liquidity
        write_key_total_ss2_lp_token_dist(scratchvar_total_ss2_lp_token_dist.load() + scratchvar_new_liquidity.load()),
        Int(1)
    ])

    on_refund = Seq([
        scratchvar_total_token2_burn_bal.store(read_protocol_unused_token2),
        Cond([
            # this AssetTransfer is for an available amount of TOKEN1
            And(
                Gtxn[2].xfer_asset() == read_key_token1,
                Gtxn[2].asset_amount() <= read_user_unused_token1(Txn.accounts[1])
            ),
           
            # USER_UNUSED_TOKEN1 = USER_UNUSED_TOKEN1 - Gtxn[2].asset_amount()
            write_user_unused_token1(
                Txn.accounts[1],
                read_user_unused_token1(Txn.accounts[1]) - Gtxn[2].asset_amount()
            ),
        ], [
            # this AssetTransfer is for an available amount of TOKEN2 by user
            And(
                Gtxn[2].xfer_asset() == read_key_token2,
                Gtxn[2].asset_amount() <= read_user_unused_token2(Txn.accounts[1]),
                Txn.application_args[0] == TRANSACTION_TYPE_REFUND
            ),
            
            # USER_UNUSED_TOKEN2 = USER_UNUSED_TOKEN2 - Gtxn[2].asset_amount()
            write_user_unused_token2(
                Txn.accounts[1],
                read_user_unused_token2(Txn.accounts[1]) - Gtxn[2].asset_amount()
            ),
        ], [
            # this AssetTransfer is for an available amount of TOKEN2 by protocol
            And(
                Gtxn[2].xfer_asset() == read_key_token2,
                Gtxn[2].asset_amount() <= scratchvar_total_token2_burn_bal.load(),
                Txn.application_args[0] == TRANSACTION_TYPE_PROTOCOL_REFUND
            ),
            # PROTOCOL_UNUSED_TOKEN2 = PROTOCOL_UNUSED_TOKEN2 - Gtxn[2].asset_amount()
            write_protocol_unused_token2(
                scratchvar_total_token2_burn_bal.load() - Gtxn[2].asset_amount()
            ),
        ], [
            # this AssetTransfer is for an available amount of SS1 LP TOKEN
            And(
                Gtxn[2].xfer_asset() == read_key_ss1_lp_token,
                Gtxn[2].asset_amount() <= read_user_unused_ss1_lp(Txn.accounts[1])
            ),
           
            # USER_UNUSED_SS1_LP_TOKEN = USER_UNUSED_SS1_LP_TOKEN -Gtxn[2].asset_amount()
            write_user_unused_ss1_lp(
                Txn.accounts[1],
                read_user_unused_ss1_lp(Txn.accounts[1]) - Gtxn[2].asset_amount()
            ),
        ], [
            # this AssetTransfer is for an available amount of SS2 LP TOKEN
            And(
                Gtxn[2].xfer_asset() == read_key_ss2_lp_token,
                Gtxn[2].asset_amount() <= read_user_unused_ss2_lp(Txn.accounts[1])
            ),
            
            # USER_UNUSED_SS2_LP_TOKEN = USER_UNUSED_SS2_LP_TOKEN - Gtxn[2].asset_amount()
            write_user_unused_ss2_lp(
                Txn.accounts[1],
                read_user_unused_ss2_lp(Txn.accounts[1]) - Gtxn[2].asset_amount()
            ),
        ]), 
        Int(1),
    ])
   
   #update state on swapping tokens
    on_other = Seq([
        key_token1_other,
        key_token2_other,
        write_key_total_token1_bal(key_token1_other.value()),
        write_key_total_token2_bal(key_token2_other.value()),
        Int(1)      
    ]) 


    program = Cond(
        [Txn.application_id() == Int(0),
            on_create],
        [Txn.on_completion() == OnComplete.CloseOut,
            on_closeout],
        [Txn.on_completion() == OnComplete.OptIn,
            on_opt_in],
        [Txn.application_args[0] == TXN_TYPE_ADD_T1_SINGLE_LP_DEPOSIT,
            on_add_single_t1_lp_deposit],
        [Txn.application_args[0] == TXN_TYPE_ADD_T2_SINGLE_LP_DEPOSIT,
            on_add_single_t2_lp_deposit],      
        [Or(Txn.application_args[0] == TXN_TYPE_SWAP_DEPOSIT_TOKEN1_TO_TOKEN2,
            Txn.application_args[0] == TXN_TYPE_SWAP_DEPOSIT_TOKEN2_TO_TOKEN1),
            on_other], 
        [Or(Txn.application_args[0] == TXN_TYPE_REFUND,
            Txn.application_args[0] == TXN_TYPE_PROTOCOL_REFUND),
            on_refund],    
    )
    return program

def clear_program():
    return Int(1)