from typing import List, Optional

from web3 import Web3
from .base_connector import BaseConnector


class NadfunConnector(BaseConnector):
    def __init__(self, rpc_url: str):
        self.rpc_url = rpc_url
        self.connect = Web3(Web3.HTTPProvider(self.rpc_url))

    def get_logs(self, from_block: int, to_block: int, address: Optional[str] = None) -> List[dict]:
        # Build params dict and omit address when not provided
        try:
            params = {"fromBlock": from_block, "toBlock": to_block}
            if address:
                params["address"] = address
            logs = self.connect.eth.get_logs(params)
            return logs
        except Exception as e:
            print("Error fetching logs:", e)
            return []