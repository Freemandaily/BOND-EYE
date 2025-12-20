"""Runtime config / secrets loader (minimal)."""
import os

def get(key, default=None):
    return os.environ.get(key, default)

settings = {
    "ENV": get("ENV", "development"),
}
