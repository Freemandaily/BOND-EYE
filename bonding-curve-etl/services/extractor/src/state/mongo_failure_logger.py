import os
import traceback
from datetime import datetime
from typing import Any, Dict, Iterable

from pymongo import MongoClient


class MongoFailureLogger:
    """Write failed extraction/decoding/sink payloads to MongoDB for later inspection."""

    def __init__(self, mongo_url: str | None = None, db_name: str | None = None, collection: str = "failed_logs"):
        if mongo_url is None:
            mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        db_name =  'BOND-EYE'

        self.client = MongoClient(mongo_url)
        self.db = self.client[db_name]
        self.collection = self.db[collection]

    def close(self):
        try:
            self.client.close()
        except Exception:
            pass


    def log_failure(self, kind: str, error: Exception, payload: Dict[str, Any] | None = None, meta: Dict[str, Any] | None = None) -> None:
        """Insert a failure document.

        Args:
            kind: short label, e.g., 'decoder', 'sink'
            error: exception instance
            payload: payload to store (e.g., logs or rows)
        """
        try:
            doc = {
                "kind": kind,
                "error": str(error),
                "traceback": traceback.format_exc(),
                "payload": payload,
                "created_at": datetime.now(),
            }
            self.collection.insert_one(doc)
        except Exception as e:
            # Logging should never raise to avoid crashing the extractor
            print("MongoFailureLogger failed to log failure:", e)
