from pyteal import *

# State Manager App IDs
STATE_MANAGER0_INDEX = Int(17786706) 
STATE_MANAGER1_INDEX = Int(17786765)

KEY_CREATOR = Bytes("C")
KEY_TOKEN1 = Bytes("T1")
KEY_TOKEN2 = Bytes("T2")
KEY_SS1_LP_TOKEN = Bytes("SSLT")
KEY_SS2_LP_TOKEN = Bytes("SSLT2")

TRANSACTION_TYPE_ADD_T1_SINGLE_LP_DEPOSIT = Bytes("a")
TRANSACTION_TYPE_ADD_T2_SINGLE_LP_DEPOSIT = Bytes("b")
TRANSACTION_TYPE_REFUND = Bytes("r")
TRANSACTION_TYPE_PROTOCOL_REFUND = Bytes("p")
TRANSACTION_TYPE_SWAP_DEPOSIT_TOKEN1_TO_TOKEN2 = Bytes("s1")
TRANSACTION_TYPE_SWAP_DEPOSIT_TOKEN2_TO_TOKEN1 = Bytes("s2")


def approval_program():

    key_token1 = App.localGetEx(Int(1), STATE_MANAGER0_INDEX, KEY_TOKEN1)
    key_token2 = App.localGetEx(Int(1), STATE_MANAGER0_INDEX, KEY_TOKEN2)
    key_ss1_lp_token = App.localGetEx(Int(1), STATE_MANAGER0_INDEX, KEY_SS1_LP_TOKEN)
    key_ss2_lp_token = App.localGetEx(Int(1), STATE_MANAGER0_INDEX, KEY_SS2_LP_TOKEN)
    
    on_create = Seq([
        App.globalPut(KEY_CREATOR, Txn.sender()),
        Int(1)
    ])

    on_closeout = Int(1)

    on_opt_in = Int(1)

    on_swap_deposit = Seq([
        key_token1,
        key_token2,
        Assert(
            And(
                # Group has 4 transactions
                Global.group_size() == Int(4),
                # This ApplicationCall is the 1st transaction
                Txn.group_index() == Int(0),
                # No additional actions are needed from this transaction
                Txn.on_completion() == OnComplete.NoOp,
                # Has one additional account attached
                Txn.accounts.length() == Int(1),
                # Has three application arguments
                Txn.application_args.length() == Int(3),

                # Second txn to state manager
                # Is of type ApplicationCall
                Gtxn[1].type_enum() == TxnType.ApplicationCall,
                # No additional actions needed
                Gtxn[1].on_completion() == OnComplete.NoOp,
                # Has one additional account attached
                Gtxn[1].accounts.length() == Int(1),
                # Has three application arguments
                Gtxn[1].application_args.length() == Int(3),
                # Additional account is same in both calls
                Txn.accounts[1] == Gtxn[1].accounts[1],
                # Application argument is same in both calls
                Txn.application_args[0] == Gtxn[1].application_args[0],
                Txn.application_args[1] == Gtxn[1].application_args[1],

                # Third txn to escrow

                # Is of type AssetTransfer
                Gtxn[2].type_enum() == TxnType.AssetTransfer,
                # Transfer asset is TOKEN1 or TOKEN2
                Or( 
                    Gtxn[2].xfer_asset() == key_token1.value(),
                    Gtxn[2].xfer_asset() == key_token2.value(), 
                ),
                # Asset sender is zero address
                Gtxn[2].asset_sender() == Global.zero_address(),
                # Asset receiver is attached account
                Gtxn[2].asset_receiver() == Txn.accounts[1],
                # Is not a close transaction
                Gtxn[2].close_remainder_to() == Global.zero_address(),
                # Is not a close asset transaction
                Gtxn[2].asset_close_to() == Global.zero_address(),
            )
        ),
        Int(1)
    ])

    on_add_lp_deposit = Seq([
        key_token1,
        key_token2,
        Assert(
            And(
                # Group has 5 transactions
                Global.group_size() == Int(5),
                # This ApplicationCall is the first transaction
                Txn.group_index() == Int(0),
                # No additional actions needed from this transaction
                Txn.on_completion() == OnComplete.NoOp,
                # Has two additional accounts attached
                Txn.accounts.length() == Int(2),
                # Has two application arguments attached
                Txn.application_args.length() == Int(2),

                # Second txn to State Manager
                # is of type ApplicationCall
                Gtxn[1].type_enum() == TxnType.ApplicationCall,
                # No additional actions needed
                Gtxn[1].on_completion() == OnComplete.NoOp,
                # Has two additional accounts attached
                Gtxn[1].accounts.length() == Int(2),
                # Has two application arguments attached
                Gtxn[1].application_args.length() == Int(2),
                # Application arguments are same as first txn
                Txn.application_args[0] == Gtxn[1].application_args[0],
                Txn.application_args[1] == Gtxn[1].application_args[1],

                # Third txn to Escrow
                # Is of type AssetTransfer
                Gtxn[2].type_enum() == TxnType.AssetTransfer,
                Or(
                    And(
                    # Transfer asset is Token 1
                    Gtxn[2].xfer_asset() == key_token1.value(),
                    # Asset receiver is the escrow account
                    Gtxn[2].asset_receiver() == Txn.accounts[1],
                    # Asset sender is zero address
                    Gtxn[2].asset_sender() == Global.zero_address(),
                    ),
                    # Transfer asset is Token 2
                    Gtxn[2].xfer_asset() == key_token2.value(),
                ),
                # Is not a close transaction
                Gtxn[2].close_remainder_to() == Global.zero_address(),
                # Is not a close asset transaction
                Gtxn[2].asset_close_to() == Global.zero_address(),

                # Fourth txn to Escrow
                # Is of type AssetTransfer
                Gtxn[3].type_enum() == TxnType.AssetTransfer,
                # Transfer asset is Token 2
                Gtxn[3].xfer_asset() == key_token2.value(),
                # Asset receiver is the escrow account
                Gtxn[3].asset_receiver() == Txn.accounts[1],
                # Is not a close transaction
                Gtxn[3].close_remainder_to() == Global.zero_address(),
                # Is not a close asset transaction
                Gtxn[3].asset_close_to() == Global.zero_address(),
            )
        ),
        Int(1)
    ])

    on_refund = Seq([
        Assert(
            And(
                # Group has 3 transactions
                Global.group_size() == Int(3),
                # This ApplicationCall is the first transaction
                Txn.group_index() == Int(0),
                # No additional actions needed from this transaction
                Txn.on_completion() == OnComplete.NoOp,
                # Has one additional account attached
                Txn.accounts.length() == Int(1),
                # Has one application argument attached
                Txn.application_args.length() == Int(1),

                # Second txn to State Manager
                # is of type ApplicationCall
                Gtxn[1].type_enum() == TxnType.ApplicationCall,
                # No additional actions needed
                Gtxn[1].on_completion() == OnComplete.NoOp,
                # Has one additional account attached
                Gtxn[1].accounts.length() == Int(1),
                # Has one application argument attached
                Gtxn[1].application_args.length() == Int(1),
                # Additional account is same as first txn
                Txn.accounts[1] == Gtxn[1].accounts[1],
                # Application argument is same as first txn
                Txn.application_args[0] == Gtxn[1].application_args[0],

                # Third txn from Escrow
                # is of type AssetTransfer
                Gtxn[2].type_enum() == TxnType.AssetTransfer,
                # sender is escrow
                Gtxn[2].sender() == Txn.accounts[1],
                # is not a clawback transaction
                Gtxn[2].asset_sender() == Global.zero_address(),
            )
        ),
        Int(1)
    ])



    program = Cond(
        [Txn.application_id() == Int(0),
            on_create],
        [Txn.on_completion() == OnComplete.CloseOut,
            on_closeout],
        [Txn.on_completion() == OnComplete.OptIn,
            on_opt_in],
        [Or(Txn.application_args[0] == TRANSACTION_TYPE_SWAP_DEPOSIT_TOKEN1_TO_TOKEN2,
            Txn.application_args[0] == TRANSACTION_TYPE_SWAP_DEPOSIT_TOKEN2_TO_TOKEN1),
            on_swap_deposit],
        [Or(Txn.application_args[0] == TRANSACTION_TYPE_ADD_T1_SINGLE_LP_DEPOSIT,
            Txn.application_args[0] == TRANSACTION_TYPE_ADD_T2_SINGLE_LP_DEPOSIT,),
            on_add_lp_deposit],     
        [Or(Txn.application_args[0] == TRANSACTION_TYPE_REFUND,
            Txn.application_args[0] == TRANSACTION_TYPE_PROTOCOL_REFUND),
            on_refund],
    )
    return program

def clear_program():
    return Int(1)
