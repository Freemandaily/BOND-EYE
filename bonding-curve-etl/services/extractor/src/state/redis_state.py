import os
import redis


class RedisState:
    """Simple Redis-backed state for last processed block."""
    def __init__(self, redis_url: str | None = None, prefix: str = "extractor"):
        # decode_responses so we get strings back
        self.client = redis.Redis(
            host='localhost',
            port=6379,
            db=2
        )
        self.key = f"{prefix}:last_block"

    def get_last_block(self) -> int | None:
        """Return last processed block or None if not set."""
        v = self.client.get(self.key)
        if v is None:
            return None
        try:
            return int(v)
        except (TypeError, ValueError):
            return None

    def set_last_block(self, block: int) -> None:
        """Set last processed block atomically."""
        self.client.set(self.key, str(int(block)))
