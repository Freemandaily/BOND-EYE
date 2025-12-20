import os
import asyncio
import sys
import time
from typing import Optional

from connectors.nadfun_connector import NadfunConnector
from decoder.decode_nadfun import decode_nadfun
from sink.postgres_sink import PostgresSink
from state.redis_state import RedisState


from fastapi import FastAPI, Request, Response
import json
import uvicorn


"""
For Manually Fetching from blocks to blocks
"""
# Config via env
RPC_URL = os.getenv("RPC_URL", "https://rpc-mainnet.monadinfra.com")
FETCH_CHUNK = int(os.getenv("FETCH_CHUNK", 100))
START_BLOCK = int(os.getenv("START_BLOCK", 41405100))
SLEEP_SECONDS = float(os.getenv("POLL_SLEEP", "5"))
ADDRESS = os.getenv("TARGET_ADDRESS")  # optional contract address filter
ADDRESS = '0xA7283d07812a02AFB7C09B60f8896bCEA3F90aCE'

app = FastAPI()

@app.get('/health')
async def health_check():
    return {'status':'active'}


@app.post("/webhook")
async def webhook_for_quickNode(request: Request):
    """
    Purpose:
        Gets Event logs From The quickNode Streaming Service
    """
    
    body_bytes = await request.body()
    body_str = body_bytes.decode()
    
    try:
        json_data = json.loads(body_str)
        asyncio.create_task(filter(json_data))
    except json.JSONDecodeError as e:
        print("Error parsing JSON:", str(e))
        print("Raw body:", body_str)

    return Response(content="Webhook received", status_code=200)

async def filter(json_data):
    decoder = decode_nadfun()
    sink = PostgresSink()

    print('Filtering For The Log Data')
    data = json_data.get('data')
    if not data:
        return 
    
    try:
        maybe_creation = await decoder.decode_for_token_creation(data)
        parsed_trades = await decoder.decode_for_token_exchange(data)
    except Exception as e:
        print("Decoder error:", e) 

    while True:
        try:
            if maybe_creation:
                sink.insert_token_creations(maybe_creation)
            if parsed_trades:
                sink.insert_token_trades(parsed_trades)
            break  
        except Exception as e:
            print("Sink error, Issue :", e)
            sink = PostgresSink() 
            continue


# if __name__ == "__main__":
#     uvicorn.run('app:app', host="0.0.0.0", port=3000, reload=True)




# async def main():
#     connector = NadfunConnector(rpc_url=RPC_URL)

#     decoder = decode_nadfun()
#     sink = PostgresSink()
#     state = RedisState()

#     last = state.get_last_block()
#     if last is None:
#         from_block = START_BLOCK
#     else:
#         from_block = last + 1

#     # main loop: poll latest block and fetch in chunks
#     while True:
#         latest = connector.connect.eth.block_number
#         if from_block > latest:
#             # nothing to do, sleep and retry
#             await asyncio.sleep(SLEEP_SECONDS)
#             continue

#         to_block = min(from_block + FETCH_CHUNK - 1, latest)
        
#         # get logs
#         logs_data = connector.get_logs(
#             from_block=from_block,
#             to_block=to_block,
#             address=ADDRESS
#         )

#         # decode results (decoder methods are async in decoder module)
#         try:
#             maybe_creation = await decoder.decode_for_token_creation(logs_data)
#             parsed_trades = await decoder.decode_for_token_exchange(logs_data)
#             # print(parsed_trades)
#         except Exception as e:
#             print("Decoder error:", e)
           

#         # persist to sink in executor (sync sink)
#         while True:
#             try:
#                 if maybe_creation:
#                     sink.insert_token_creations(maybe_creation)
#                 if parsed_trades:
#                     sink.insert_token_trades(parsed_trades)
#                 break  
#             except Exception as e:
#                 print("Sink error, Issue :", e)
#                 sink = PostgresSink()  # re-init sink on error
#                 continue

#         # on success, update last processed block in Redis
#         state.set_last_block(to_block)

#         # advance
#         from_block = to_block + 1

# if __name__ == "__main__":
#     import asyncio

#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         print("Interrupted, exiting")


