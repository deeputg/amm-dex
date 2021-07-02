from pyteal import *

def logicsig():
    
    on_add_single_t1_lp_deposit = And(
        Gtxn[0].type_enum() == TxnType.ApplicationCall,
        Gtxn[0].application_id() == Int(txn_verifier_id),
        Gtxn[0].on_completion() == OnComplete.NoOp,
       
        Gtxn[1].type_enum() == TxnType.ApplicationCall,
        Gtxn[1].application_id() == Int(state_manager0_id),
        Gtxn[1].on_completion() == OnComplete.NoOp,

        Gtxn[2].type_enum() == TxnType.AssetTransfer,
        Gtxn[2].xfer_asset() == Int(token1_id),
        Gtxn[2].asset_close_to() == Global.zero_address(),
        Gtxn[2].rekey_to() == Global.zero_address(),
        
        Gtxn[3].type_enum() == TxnType.AssetTransfer,
        Gtxn[3].xfer_asset() == Int(token2_id),
        Gtxn[3].asset_close_to() == Global.zero_address(),
        Gtxn[3].rekey_to() == Global.zero_address(),

        Gtxn[4].type_enum() == TxnType.ApplicationCall,
        Gtxn[4].application_id() == Int(state_manager1_id),
        Gtxn[4].on_completion() == OnComplete.NoOp,    
    )

    program = Cond(
        [Global.group_size() == Int(5), on_add_single_t1_lp_deposit]
    )

    return compileTeal(program, Mode.Signature)

state_manager0_id = 17786706
state_manager1_id = 17786765
txn_verifier_id = 17786816
token1_id = 17782775
token2_id = 17782776

if __name__ == "__main__":
    with open('build/developer_lsig.teal', 'w') as f:
        compiled = logicsig()
        f.write(compiled)
