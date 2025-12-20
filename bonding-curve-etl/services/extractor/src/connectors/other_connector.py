from .base_connector import BaseConnector

class OtherConnector(BaseConnector):
    def connect(self):
        return True

    def fetch(self):
        return []
