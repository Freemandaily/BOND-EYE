from pydantic import BaseModel

class NadfunCreatedEvent(BaseModel):
    deployer_address:str
    token_address:str
    fee_reciever:str
    deployer_bought_amount:int
    tx_hash:str


class NadfunExchangedEvent(BaseModel):
    trader:str
    token_address:str
    amount:int
    trade_direction:str
    tx_hash:str