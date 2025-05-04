from pyteal import *

def rental_contract():
    rent_pool = Bytes("rent_pool")  # global state

    on_create = Seq([
        App.globalPut(rent_pool, Int(0)),
        Return(Int(1))
    ])

    on_deposit = Seq([
        Assert(Global.group_size() == Int(2)),
        Assert(Gtxn[1].type_enum() == TxnType.Payment),
        Assert(Gtxn[1].receiver() == Global.current_application_address()),
        App.globalPut(rent_pool, App.globalGet(rent_pool) + Gtxn[1].amount()),
        Return(Int(1))
    ])

    on_call = Cond(
        [Txn.application_id() == Int(0), on_create],
        [Txn.application_args[0] == Bytes("deposit_rent"), on_deposit]
    )

    return on_call

if __name__ == "__main__":
    compiled = compileTeal(rental_contract(), mode=Mode.Application, version=6)
    with open("rental_contract.teal", "w") as f:
        f.write(compiled)
