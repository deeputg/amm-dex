from pyteal import *

state_manager0_app_id = Int(17786706)
state_manager1_app_id = Int(17786765)
txn_verifier_app_id = Int(17786816)
token1_asset_id = Int(17782775) 
token2_asset_id = Int(17782776)
ss1_liquidity_token_asset_id = Int(17786839)
ss2_liquidity_token_asset_id = Int(17786865)
optin_last_valid = Int(90000000) 

def logicsig():
    program = Cond(
        [
            # If there is a single transaction within the group
            Global.group_size() == Int(1),
            # Then either this is an opt-in to a contract, or to an asset
            Or(
                And(
                    # This is a contract opt-in transaction
                    Txn.on_completion() == OnComplete.OptIn,
                    # Transaction's last valid round is lte specified last valid round
                    Txn.last_valid() <= optin_last_valid,
                    Or(
                        # Is an opt in to the verifier contract
                        Txn.application_id() == txn_verifier_app_id,
                        # Is an opt in to the state manager contracts
                        Txn.application_id() == state_manager0_app_id,
                        Txn.application_id() == state_manager1_app_id
                    )
                ),
                And(
                    # This is an asset opt-in
                    Txn.type_enum() == TxnType.AssetTransfer,
                    # Sender and asset receiver are both Escrow
                    Txn.sender() == Txn.asset_receiver(),
                    # Transaction's last valid round is lte specified last valid round
                    Txn.last_valid() <= optin_last_valid,
                    # Is an opt-in to one of the expected assets
                    Or(
                        # Is an opt in to Token 1 Asset
                        Txn.xfer_asset() == token1_asset_id,
                        # Is an opt in to Token 2 Asset
                        Txn.xfer_asset() == token2_asset_id,
                        # Is an opt in to Single side Liquidit Token Asset
                        Txn.xfer_asset() == ss1_liquidity_token_asset_id,
                        # Is an opt in to other Single side Liquidity Token Asset
                        Txn.xfer_asset() == ss2_liquidity_token_asset_id,

                    )
                ),
            )
        ],
        [
            # If there are three transactions within the group
            Global.group_size() == Int(3),
            # Then this is a refund transaction
            And(
                # first one is an ApplicationCall
                Gtxn[0].type_enum() == TxnType.ApplicationCall,
                # the ApplicationCall must be approved by the verifier  application
                Gtxn[0].application_id() == txn_verifier_app_id,

                # second one is an ApplicationCall
                Gtxn[1].type_enum() == TxnType.ApplicationCall,
                # Must be approved by either state manager application
                Or(
                    Gtxn[1].application_id() == state_manager0_app_id,
                    Gtxn[1].application_id() == state_manager1_app_id,
                ),

                # this transaction is the third one
                Txn.group_index() == Int(2),
                # this transaction is an AssetTransfer
                Txn.type_enum() == TxnType.AssetTransfer,
                # this transaction is not a close transaction
                Txn.close_remainder_to() == Global.zero_address(),
                # this transaction is not an asset close transaction
                Txn.asset_close_to() == Global.zero_address()
            )
        ],
        [
            # If there are five transactions within the group
            Global.group_size() == Int(5),
            # Then this is to Add single side DEX token liquidity
            And(
                # first one is an ApplicationCall
                # first one is an ApplicationCall
                Gtxn[0].type_enum() == TxnType.ApplicationCall,
                # the ApplicationCall must be approved by the verifier application
                Gtxn[0].application_id() == txn_verifier_app_id,

                # second one is an ApplicationCall
                Gtxn[1].type_enum() == TxnType.ApplicationCall,
                # Must be approved by the state manager application
                Gtxn[1].application_id() == state_manager0_app_id,

                # this transaction is the third or fourth one
                Or(
                    Txn.group_index() == Int(2),
                    Txn.group_index() == Int(3),
                ),
                # this transaction is an AssetTransfer
                Txn.type_enum() == TxnType.AssetTransfer,
                # this transaction is not a close transaction
                Txn.close_remainder_to() == Global.zero_address(),
                # this transaction is not an asset close transaction
                Txn.asset_close_to() == Global.zero_address(),
            )
        ]
    )
    return program


if __name__ == "__main__":
    with open('build/escrow_lsig.teal', 'w') as f:
        program = logicsig()
        compiled = compileTeal(program, Mode.Signature)
        f.write(compiled)
