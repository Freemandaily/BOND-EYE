from pydantic import BaseModel

class RawEvent(BaseModel):
    tx_hash: str
    data: dict
