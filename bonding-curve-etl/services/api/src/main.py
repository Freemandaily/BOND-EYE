from fastapi import FastAPI

app = FastAPI(title="bonding-curve-api")

@app.get("/health")
def health():
    return {"status": "ok"}
