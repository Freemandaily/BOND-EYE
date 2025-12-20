from abc import ABC, abstractmethod

class BaseConnector(ABC):

    @abstractmethod
    def get_logs(self, from_block: int, to_block: int, address: str):
        pass