from .base_connector import BaseConnector

class PumpfunConnector(BaseConnector):
    def connect(self):
        return True

    def fetch(self):
        # placeholder: return empty list of events
        return []


# fetch through websocket or through blocks