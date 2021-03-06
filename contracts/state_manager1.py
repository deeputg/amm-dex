from pyteal import *

STATE_MANAGER0_INDEX = Int(18167705)

KEY_TOTAL_TOKEN1_BAL = Bytes("B1")
KEY_TOTAL_TOKEN2_BAL = Bytes("B2")
KEY_TOTAL_SS1_LP_TOKEN_DIST = Bytes("LD1")
KEY_TOTAL_SS2_LP_TOKEN_DIST = Bytes("LD2")
KEY_TOTAL_TOKEN2_MINTED_BAL = Bytes("B2M")
KEY_TOTAL_TOKEN2_TO_BURN = Bytes("BURN")

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
    
    # Write to additional account
    def write_key_total_token1_bal(bal: Int): return App.localPut(Int(1), KEY_TOTAL_TOKEN1_BAL, bal)
    def write_key_total_token2_bal(bal: Int): return App.localPut(Int(1), KEY_TOTAL_TOKEN2_BAL, bal)
    def write_key_total_token2_minted_bal(bal: Int): return App.localPut(Int(1), KEY_TOTAL_TOKEN2_MINTED_BAL, bal)
    def write_key_total_ss1_lp_token_dist(bal: Int): return App.localPut(Int(1), KEY_TOTAL_SS1_LP_TOKEN_DIST, bal)
    def write_key_total_ss2_lp_token_dist(bal: Int): return App.localPut(Int(1), KEY_TOTAL_SS2_LP_TOKEN_DIST, bal)
    def write_protocol_unused_token2(bal: Int): return App.localPut(Int(1), KEY_TOTAL_TOKEN2_TO_BURN, bal)
    
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
    scratchvar_total_ss1_lp_token_dist = ScratchVar(TealType.uint64)
    scratchvar_total_ss2_lp_token_dist = ScratchVar(TealType.uint64)
    scratchvar_new_liquidity = ScratchVar(TealType.uint64)
    scratchvar_temp = ScratchVar(TealType.uint64)
    scratchvar_temp_token2_used = ScratchVar(TealType.uint64)
    scratchvar_total_token2_minted_bal = ScratchVar(TealType.uint64)
    scratchvar_total_token2_burn_bal = ScratchVar(TealType.uint64)
    scratchvar_swap_token2_output = ScratchVar(TealType.uint64)
    scratchvar_swap_token1_output = ScratchVar(TealType.uint64)

    key_token1_other = App.localGetEx(Int(1), STATE_MANAGER0_INDEX, KEY_TOTAL_TOKEN1_BAL)
    key_token2_other = App.localGetEx(Int(1), STATE_MANAGER0_INDEX, KEY_TOTAL_TOKEN2_BAL)
    
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

    def swap_token_output_minus_fees(asset_amount: Int): return (asset_amount * Int(997)) / Int(1000)

    def swap_token2_output(token1_input: Int):
        return read_key_total_token2_bal - (read_key_total_token1_bal * read_key_total_token2_bal) / (read_key_total_token1_bal + token1_input)

    on_swap_deposit = Seq([
        scratchvar_swap_token2_output.store(swap_token_output_minus_fees(swap_token2_output(Gtxn[2].asset_amount()))),
        
        # Assert token2_output >= min_token2_required_by_user
        Assert(
            scratchvar_swap_token2_output.load() >= Btoi(Txn.application_args[1])
        ),
        # USER_UNUSED_TOKEN2 = USER_UNUSED_TOKEN2 + token2_output
        write_user_unused_token2(
            Txn.accounts[1],
            read_user_unused_token2(Txn.accounts[1]) + scratchvar_swap_token2_output.load()
        ),
       
        # TOTAL_TOKEN1_BALANCE = TOTAL_TOKEN1_BALANCE + token1_input
        write_key_total_token1_bal(
            read_key_total_token1_bal + Gtxn[2].asset_amount()
        ),

        # TOTAL_TOKEN2_BALANCE = TOTAL_TOKEN2_BALANCE + token2_fees - token2_output 
        write_key_total_token2_bal(
            (read_key_total_token2_bal + ((Gtxn[2].asset_amount() * Int(997)) / Int(1000))) 
                                                                      - scratchvar_swap_token2_output.load()
        ),
        
        Int(1)
    ])

    def swap_token1_output(token2_input: Int):
        return read_key_total_token1_bal - (read_key_total_token1_bal * read_key_total_token2_bal) / (read_key_total_token2_bal + token2_input)

    on_swap_deposit_2 = Seq([
        scratchvar_swap_token1_output.store(swap_token_output_minus_fees(swap_token1_output(Gtxn[2].asset_amount()))),
        
        # Assert token2_output >= min_token2_required_by_user
        Assert(
            scratchvar_swap_token1_output.load() >= Btoi(Txn.application_args[1])
        ),

        # USER_UNUSED_TOKEN2 = USER_UNUSED_TOKEN2 + token2_output
        write_user_unused_token1(
            Txn.accounts[1],
            read_user_unused_token1(Txn.accounts[1]) + scratchvar_swap_token1_output.load()
        ),
       
        # TOTAL_TOKEN1_BALANCE = TOTAL_TOKEN1_BALANCE + token1_fees - token1_output 
        write_key_total_token1_bal(
            (read_key_total_token1_bal + ((Gtxn[2].asset_amount() * Int(997)) / Int(1000))) 
                                                                      - scratchvar_swap_token1_output.load()
        ),

        # TOTAL_TOKEN2_BALANCE = TOTAL_TOKEN2_BALANCE + token2_input
        write_key_total_token2_bal(
            read_key_total_token2_bal + Gtxn[2].asset_amount()
        ),
        
        Int(1)
    ])

    
    on_refund = Seq([
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
                Txn.application_args[0] == TXN_TYPE_REFUND
            ),
            
            # USER_UNUSED_TOKEN2 = USER_UNUSED_TOKEN2 - Gtxn[2].asset_amount()
            write_user_unused_token2(
                Txn.accounts[1],
                read_user_unused_token2(Txn.accounts[1]) - Gtxn[2].asset_amount()
            ),
        ]), 

        Int(1),
    ])
   
    #Update state on addition of liquidity
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
        [Txn.application_args[0] == TXN_TYPE_SWAP_DEPOSIT_TOKEN1_TO_TOKEN2,
            on_swap_deposit],
        [Txn.application_args[0] == TXN_TYPE_SWAP_DEPOSIT_TOKEN2_TO_TOKEN1,
            on_swap_deposit_2],
        [Txn.application_args[0] == TXN_TYPE_REFUND,
            on_refund],    
        [Or(Txn.application_args[0] == TXN_TYPE_ADD_T1_SINGLE_LP_DEPOSIT,
            Txn.application_args[0] == TXN_TYPE_ADD_T2_SINGLE_LP_DEPOSIT),
            on_other],    
        
    )
    return program

def clear_program():
    return Int(1)


if __name__ == "__main__":
    state_manager1_approve_teal_code = compileTeal(approval_program(), Mode.Application)
    with open('./build/state_manager1_approval.teal', 'w') as f:
        f.write(state_manager1_approve_teal_code)
    state_manager1_clear_teal_code = compileTeal(clear_program(), Mode.Application)    
    with open('./build/state_manager1_clear.teal', 'w') as f:
        f.write(state_manager1_clear_teal_code)    