from algosdk import account, algod, transaction
from algosdk.v2client import algod
from algosdk.future.transaction import AssetConfigTxn

algod_token = "YOUR_ALGOD_TOKEN"
algod_address = "http://localhost:4001"
algod_client = algod.AlgodClient(algod_token, algod_address)

creator_mnemonic = "your 25-word mnemonic here"
creator_private_key = account.mnemonic_to_private_key(creator_mnemonic)
creator_address = account.address_from_private_key(creator_private_key)

params = algod_client.suggested_params()

txn = AssetConfigTxn(
    sender=creator_address,
    sp=params,
    total=10000,
    decimals=0,
    default_frozen=False,
    unit_name="PROP",
    asset_name="PropertyToken",
    manager=creator_address,
    reserve=creator_address,
    freeze=None,
    clawback=None
)

signed_txn = txn.sign(creator_private_key)
txid = algod_client.send_transaction(signed_txn)
print("ASA Creation TX ID:", txid)
